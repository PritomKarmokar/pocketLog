import secrets

from django.conf import settings

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounts.models import User, PasswordChangeRequest
from applibs.logger import get_logger
from applibs.helper import generate_hashed_token
from applibs.response import format_output_success, format_output_error
from accounts.serializers import (
    AddPasswordSerializer, 
    ResetPasswordSerializer,
    RequestForgotPasswordSerializer
)
from applibs.status import (
    VALID_DATA_NOT_FOUND,
    PASSWORD_RESET_SUCCESS,
    PASSWORD_ASSERT_SUCCESS,
    PASSWORD_DOES_NOT_MATCH,
    PASSWORD_REQUEST_PROCESS_FAILED,
    INVALID_PASSWORD_ASSERT_OPTIONS,
    PASSWORD_REQUEST_LINK_SENT_SUCCESS,
)

logger = get_logger(__name__)

class AddPasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddPasswordSerializer

    def post(self, request: Request) -> Response:
        user = request.user
        if user.has_usable_password():
            logger.error("User already has active password")
            return Response(INVALID_PASSWORD_ASSERT_OPTIONS, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            errors = serializer.errors
            logger.error("Add Password Serializer Errors: %s", errors)
            return Response(format_output_error(VALID_DATA_NOT_FOUND, error=errors), status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        password = validated_data.get('password')

        _ = user.add_password(password)
        logger.info("Password added successfully")
        return Response(PASSWORD_ASSERT_SUCCESS, status=status.HTTP_200_OK)

class ResetPasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ResetPasswordSerializer

    def post(self, request: Request) -> Response:
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            errors = serializer.errors
            logger.warning("Reset Password Serializer Errors: %s", errors)
            return Response(
                format_output_error(VALID_DATA_NOT_FOUND, error=errors), status=status.HTTP_400_BAD_REQUEST
            )

        validated_data = serializer.validated_data
        old_password = validated_data.get('password')
        new_password = validated_data.get('new_password')

        if not user.check_password(old_password):
            logger.error("User has entered wrong password")
            return Response(PASSWORD_DOES_NOT_MATCH, status=status.HTTP_400_BAD_REQUEST)

        _ = user.set_password(new_password)
        logger.info("Password reset successful")
        return Response(PASSWORD_RESET_SUCCESS, status=status.HTTP_200_OK)


class RequestForgotPasswordAPIView(APIView):
    permission_classes = []
    serializer_class = RequestForgotPasswordSerializer
    
    def post(self, request: Request) -> Response:
        data = request.data
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            errors = serializer.errors
            logger.error("Request Forgot Password Serializer Errors: %s", errors)
            return Response(VALID_DATA_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        email = validated_data.get('email')

        user = User.objects.fetch_user_with_email(email=email)
        if not user:
            logger.error("User with given email %s doesn't exist", email)
            # todo: instead of this, return a success response depicting password reset email will be sent if the email exists
            return Response(VALID_DATA_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST) 
        
        
        token = secrets.token_urlsafe(32)
        hashed_token = generate_hashed_token(token)
        new_request = PasswordChangeRequest.objects.create_new_request(
            hashed_token=hashed_token,
            user_id=user.id,
        )
        if not new_request:
            logger.error("Failed to create PasswordChangeRequest for user_id: %s", user.id)
            return Response(PASSWORD_REQUEST_PROCESS_FAILED, status=status.HTTP_400_BAD_REQUEST)
        
        base_url = settings.POCKET_LOG_BASE_URL
        reset_link = f"{base_url}/reset-password?token={token}"
        
        # todo: send email to user with this reset_link, and change the response accordingly
        response_data = {
            "reset_link": reset_link
        }
        return Response(
            format_output_success(PASSWORD_REQUEST_LINK_SENT_SUCCESS, data=response_data),
            status=status.HTTP_200_OK
        )