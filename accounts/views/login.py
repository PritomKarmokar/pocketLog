from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from django.conf import settings
from django.contrib.auth import authenticate

from accounts.models import User
from applibs.logger import get_logger
from applibs.helper import render_serializer_errors
from applibs.status import (
    USER_LOGIN_SUCCESS,
    INVALID_CREDENTIALS,
    INVALID_LOGIN_OPTIONS,
)
from accounts.serializers import LoginSerializer
from applibs.response import format_output_success

logger = get_logger(__name__)

class LoginAPIView(APIView):
    permission_classes = []
    serializer_class = LoginSerializer

    def post(self, request: Request)-> Response:
        data = request.data
        serializer = self.serializer_class(data=data)

        if not serializer.is_valid():
            errors = serializer.errors
            logger.error("Login Serializer Errors: %s", errors)
            return Response(render_serializer_errors(errors), status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        email = validated_data.get('email')
        password = validated_data.get('password')

        user = User.objects.fetch_user_with_email(email=email)
        if not user:
            logger.error("User with email %s does not exists", email)
            return Response(INVALID_CREDENTIALS, status=status.HTTP_401_UNAUTHORIZED)

        if not user.has_usable_password():
            logger.error("User with email %s has unusable password", email)
            return Response(INVALID_LOGIN_OPTIONS, status=status.HTTP_400_BAD_REQUEST)

        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            response_data = {
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "header_token": settings.SIMPLE_JWT.get("AUTH_HEADER_TYPES"),
                "expires_in": int(refresh.lifetime.total_seconds())
            }
            return Response(format_output_success(USER_LOGIN_SUCCESS, response_data), status=status.HTTP_200_OK)

        return Response(INVALID_CREDENTIALS, status=status.HTTP_401_UNAUTHORIZED)