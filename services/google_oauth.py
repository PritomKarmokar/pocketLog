import secrets
import requests

from typing import Any, Optional
from rest_framework import status

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
    def get_headers(
        token: str,
        token_type: str = "Bearer",
    ) -> dict:
        headers = {
            "Authorization": f"{token_type} {token}"
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
    ) -> Optional[dict[str, Any]]:
        payload = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        response = requests.post(self.token_url, data=payload, timeout=self.timeout)

        response_data = response.json()
        response_code = response.status_code

        if status.is_success(response_code):
            logger.info({
                "Google Token Response Status Code": response_code,
                "Response": response_data,
            })
            return response_data
        else:
            logger.error({
                "Error": "Google Token Exchange Failed",
                "Response": response_data or {},
            })
            return None

    def get_user_info(
        self,
        token_type: str,
        access_token: str
    ) -> Optional[dict[str, Any]]:

        headers = self.get_headers(access_token, token_type)
        response = requests.get(self.user_info_url, headers=headers, timeout=self.timeout)

        response_data = response.json()
        response_code = response.status_code
        if status.is_success(response_code):
            logger.info({
                "Google User Info Response Status Code": response_code,
                "Response": response_data,
            })
            return response_data
        else:
            logger.error({
                "Error": "Google User Info Fetch Failed",
                "Response": response_data or {},
            })
            return None