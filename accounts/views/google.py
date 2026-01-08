from django.shortcuts import redirect

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from applibs.logger import get_logger
from services.google_oauth import GoogleOAuth

logger = get_logger(__name__)

class GoogleLoginRedirectAPIView(APIView):
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
            return Response(
                {"error": "Invalid state or code"},
                status=status.HTTP_400_BAD_REQUEST
            )

        token_response = self.oauth.exchange_code_for_token(code)
        user_info = self.oauth.get_user_info(token_response['access_token'])

        email = user_info.get('email')
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': user_info.get('name'),
                'first_name': user_info.get('given_name', ''),
                'last_name': user_info.get('family_name', '')
            }
        )

        if user:
            refresh = RefreshToken.for_user(user)
            response_dict = {
                "message": f"Google Login Successful for user {user.username}",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            }
            return Response(data=response_dict, status=status.HTTP_200_OK)

        return Response(
            {"error": "Google Login Failed"},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )