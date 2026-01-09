from django.urls import path

from .views import (
    GoogleLoginAPIView,
    GoogleCallBackAPIView,
    SignUpAPIView,
    LoginAPIView,
    LogOutAPIView,
    AddPasswordAPIView,
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
    path(
        "logout/",
        LogOutAPIView.as_view(),
        name="logout"
    ),
    path(
        "add-password/",
        AddPasswordAPIView.as_view(),
        name="add_password",
    )
]