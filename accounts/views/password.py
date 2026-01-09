from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from applibs.logger import get_logger
from accounts.serializers import AddPasswordSerializer
from applibs.status import (
    VALID_DATA_NOT_FOUND,
    PASSWORD_ASSERT_SUCCESS,
    PASSWORDS_DOES_NOT_MATCH,
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
            return Response(VALID_DATA_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        password = validated_data.get('password')
        confirm_password = validated_data.get('confirm_password')

        if password != confirm_password:
            logger.error("Passwords do not match")
            return Response(PASSWORDS_DOES_NOT_MATCH, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()
        logger.info("Password added successfully")
        return Response(PASSWORD_ASSERT_SUCCESS, status=status.HTTP_200_OK)
