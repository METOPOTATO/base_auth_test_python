from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.views import ObtainJSONWebToken

from .models import User
from .utils.mail_handler import create_verify_email
from .serializers import UserSerializer
from .utils.messages import RESPONSE_ERRORS, RESPONSE_OK
from rest_framework import status
# Create your views here.


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            create_verify_email(user, [user.email])
            return Response(serializer.data)

        return Response(status=status.HTTP_400_BAD_REQUEST, data={'result': RESPONSE_ERRORS.INVALID_DATA})


class LoginView(ObtainJSONWebToken):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'result': RESPONSE_ERRORS.USER_NOT_FOUND})

        if not user.check_password(password):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'result': RESPONSE_ERRORS.WRONG_PW})

        return super().post(request, *args, **kwargs)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_serializer = UserSerializer(request.user)
        return Response(user_serializer.data)


class EmailVerifyView(APIView):
    authentication_classes = []
    permission_classes = []

    # get token
    def get(self, request):
        token = request.data['token']
        user = User.objects.filter(token=token, is_active=False).first()
        if user:
            user.is_active = True
            user.save()
            return Response({'Result': RESPONSE_OK.DEFAULT})
        return Response(status=status.HTTP_404_NOT_FOUND, data={'result': RESPONSE_ERRORS.USER_NOT_FOUND})
