from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from applibs.logger import get_logger
from applibs.response import format_output_success, format_output_error
from accounts.serializers import AddPasswordSerializer, ResetPasswordSerializer
from applibs.status import (
    VALID_DATA_NOT_FOUND,
    PASSWORD_RESET_SUCCESS,
    PASSWORD_ASSERT_SUCCESS,
    PASSWORD_DOES_NOT_MATCH,
    INVALID_PASSWORD_ASSERT_OPTIONS
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
