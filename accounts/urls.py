from django.urls import path

from .views import (
    GoogleLoginAPIView,
    GoogleCallBackAPIView,
    SignUpAPIView,
    LoginAPIView,
)

urlpatterns = [
    path(
        "google/login/",
        GoogleLoginAPIView.as_view(),
        name="google_login"
    ),
    path(
        "google/callback/",
        GoogleCallBackAPIView.as_view(),
        name="google_callback"
    ),
    path(
        "signup/",
        SignUpAPIView.as_view(),
        name="signup"
    ),
    path(
        "login/",
        LoginAPIView.as_view(),
        name="login"
    ),
]