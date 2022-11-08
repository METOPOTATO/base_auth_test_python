from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.views import ObtainJSONWebToken

from .models import User
from .serializers import UserSerializer
from .utils.mail_handler import create_verify_email
from .utils.messages import RESPONSE_ERRORS, RESPONSE_OK, VALIDATION_ERRORS

# Create your views here.


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        email = request.data['email']
        exist_user = User.objects.filter(email=email)
        if len(exist_user) >= 1:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'Error': RESPONSE_ERRORS.EMAIL_EXIST})
        
        if serializer.is_valid():
            user = serializer.save()
            create_verify_email(user, [user.email])
            return Response(serializer.data)
        elif 'non_field_errors' in serializer.errors and serializer.errors['non_field_errors'][0] == VALIDATION_ERRORS.INVALID_EMAIL_FORM:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'Error': VALIDATION_ERRORS.INVALID_EMAIL_FORM})
        elif 'non_field_errors' in serializer.errors and serializer.errors['non_field_errors'][0] == VALIDATION_ERRORS.PASSWORD_TOO_SHORT:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'Error': VALIDATION_ERRORS.PASSWORD_TOO_SHORT})
        
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'Error': serializer.errors})


class LoginView(ObtainJSONWebToken):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'Error': RESPONSE_ERRORS.USER_NOT_FOUND})

        if not user.check_password(password):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'Error': RESPONSE_ERRORS.WRONG_PW})

        if user.is_active == False:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'Error': RESPONSE_ERRORS.USER_IS_NOT_ACTIVE})

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
        token = request.query_params['token']
        user = User.objects.filter(token=token, is_active=False).first()
        if user:
            user.is_active = True
            user.save()
            return Response({'Result': RESPONSE_OK.DEFAULT})
        return Response(status=status.HTTP_404_NOT_FOUND, data={'Error': RESPONSE_ERRORS.TOKEN_NOT_FOUNDED})
