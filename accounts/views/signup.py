from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from accounts.models import User
from applibs.logger import get_logger
from accounts.serializers import SignUpSerializer
from applibs.status import  (
    USER_SIGNUP_SUCCESS,
    USER_CREATION_FAILED,
)
from applibs.response import format_output_success
from applibs.helper import render_serializer_errors

logger = get_logger(__name__)

class SignUpAPIView(APIView):
    permission_classes = []
    serializer_class = SignUpSerializer

    def post(self, request: Request) -> Response:
        data = request.data
        serializer = self.serializer_class(data=data)

        if not serializer.is_valid():
            errors = serializer.errors
            logger.error("SignUp Serializer Errors: %s", errors)
            return Response(render_serializer_errors(errors), status=status.HTTP_400_BAD_REQUEST)

        serializer_data = serializer.validated_data
        user = User.objects.create_user(**serializer_data)
        if not user:
            logger.error("Error occurred while creating new user")
            return Response(USER_CREATION_FAILED, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            format_output_success(USER_SIGNUP_SUCCESS, data=user.profile_response_data), status=status.HTTP_201_CREATED
        )