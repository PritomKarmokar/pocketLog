import secrets
import requests

from django.conf import settings
from urllib.parse import urlencode

from applibs.logger import get_logger

logger = get_logger(__name__)

class GoogleOAuth:
    def __init__(self):
        super().__init__()
        self.timeout = settings.REQUEST_TIMEOUT
        self.auth_url = settings.GOOGLE_AUTH_URL
        self.token_url = settings.GOOGLE_TOKEN_URL
        self.user_info_url = settings.GOOGLE_USER_INFO_URL

    @staticmethod
    def generate_state():
        return secrets.token_urlsafe(16)

    @staticmethod
    def get_headers(token: str) -> dict:
        headers = {
            "Authorization": f"Bearer {token}"
        }
        return headers

    def get_authorization_url(
        self,
        state: str
    ) -> str:
        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "scope": "openid email profile",
            "state": state,
            "access_type": "offline",
            "prompt": "select_account"
        }
        auth_url = f"{self.auth_url}?{urlencode(params)}"
        logger.info(f"Google Authorization URL: {auth_url}")
        return auth_url

    def exchange_code_for_token(
        self,
        code: str
    ) -> dict:
        data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        response = requests.post(self.token_url, data=data, timeout=self.timeout)

        logger.info({
            "Google Token Response": response.json(),
            "status_code": response.status_code,
        })

        return response.json()

    def get_user_info(
        self,
        access_token: str
    ) -> dict:
        headers = self.get_headers(access_token)
        response = requests.get(self.user_info_url, headers=headers, timeout=self.timeout)

        logger.info({
            "Google User Info Response": response.json(),
            "status_code": response.status_code,
        })
        return response.json()