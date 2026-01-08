from django.urls import path

from .views import (
    GoogleCallBackAPIView,
    GoogleLoginRedirectAPIView
)

urlpatterns = [
    path(
        "google/redirect/",
        GoogleLoginRedirectAPIView.as_view(),
        name="google_login_redirect"
    ),
    path(
        "google/callback/",
        GoogleCallBackAPIView.as_view(),
        name="google_callback"
    ),
]