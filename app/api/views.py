from multiprocessing import AuthenticationError

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.views import ObtainJSONWebToken

from .models import User
from .utils.mail_handler import create_verify_email
from .serializers import UserSerializer
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
# Create your views here.


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(data='Error')


class LoginView(ObtainJSONWebToken):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationError('User is not found')

        if not user.check_password(password):
            raise AuthenticationError('Incorrect password')

        return super().post(request, *args, **kwargs)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_serializer = UserSerializer(request.user)
        return Response(user_serializer.data)


class EmailVerifyView(APIView):
    authentication_classes = []
    permission_classes = []
    # generate a token and send to email to verify

    def post(self, request):
        email = request.data['email']
        user = User.objects.filter(email=email).first()
        if user:
            create_verify_email(user, [user.email])
            return Response({'Result': 'OK'})
        return Response({'Result': 'User is not found'})

    # get token
    def get(self, request):
        token = request.data['token']
        user = User.objects.filter(token=token, is_active=False).first()
        if user:
            user.is_active = True
            user.save()
            return Response({'Result': 'OK'})
        return Response({'Result': token})
