from django.conf import settings
from django.shortcuts import redirect

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from applibs.logger import get_logger
from services.google_oauth import GoogleOAuth
from applibs.response import format_output_success
from applibs.status import (
    GOOGLE_LOGIN_SUCCESS,
    GOOGLE_LOGIN_FAILED,
    INVALID_STATE_OR_CODE,
    GOOGLE_TOKEN_FETCH_FAILED,
    GOOGLE_USER_INFO_FETCH_FAILED
)

logger = get_logger(__name__)

class GoogleLoginAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def __init__(self):
        super().__init__()
        self.oauth = GoogleOAuth()

    def get(self, request: Request):
        state = self.oauth.generate_state()
        request.session['google_oauth_state'] = state
        auth_url = self.oauth.get_authorization_url(state)
        return redirect(auth_url)

class GoogleCallBackAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def __init__(self):
        super().__init__()
        self.oauth = GoogleOAuth()

    def get(self, request: Request) -> Response:
        request_data = request.GET
        code = request_data.get('code')
        state = request_data.get('state')
        saved_state = request.session.get('google_oauth_state')

        if not code or not state or state != saved_state:
            logger.error({"Error": "Invalid state or code",})
            return Response(INVALID_STATE_OR_CODE, status=status.HTTP_400_BAD_REQUEST)

        token_response = self.oauth.exchange_code_for_token(code)
        if not token_response:
            return Response(GOOGLE_TOKEN_FETCH_FAILED, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        token_type = token_response.get('token_type')
        access_token = token_response.get('access_token')

        user_info = self.oauth.get_user_info(token_type, access_token)
        if not user_info:
            return Response(GOOGLE_USER_INFO_FETCH_FAILED, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        email = user_info.get('email')
        user = User.objects.fetch_user_with_email(email)
        if not user:
            user = User.objects.create_user(
                email = email,
                username = user_info.get('name'),
                first_name = user_info.get('given_name', ''),
                last_name = user_info.get('family_name', ''),
                auth_provider = 'google',
            )

        if user:
            _ = user.mark_logged_in()
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            response_data = {
                "access_token": str(access_token),
                "refresh_token": str(refresh),
                "header_token": settings.SIMPLE_JWT.get("AUTH_HEADER_TYPES"),
                "expires_in": int(refresh.lifetime.total_seconds()),
                "token_type": "Bearer"
            }
            return Response(
                format_output_success(GOOGLE_LOGIN_SUCCESS, response_data), status=status.HTTP_200_OK
            )

        return Response(GOOGLE_LOGIN_FAILED, status=status.HTTP_422_UNPROCESSABLE_ENTITY)