from django.urls import path

from .views import (
    GoogleLoginAPIView,
    GoogleCallBackAPIView,
    SignUpAPIView
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
    )
]