from django.urls import path

from .views import (
    GoogleLoginAPIView,
    GoogleCallBackAPIView,
    SignUpAPIView,
    LoginAPIView,
    LogOutAPIView,
    AddPasswordAPIView,
    ResetPasswordAPIView,
    ForgotPasswordPageView,
    RequestForgotPasswordAPIView,
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
    ),
    path(
        "reset-password/",
        ResetPasswordAPIView.as_view(),
        name="reset_password",
    ),
    path(
        "request/forgot-password/",
        RequestForgotPasswordAPIView.as_view(),
        name="request_forgot_password",
    ),
    path(
        "forgot-password/",
        ForgotPasswordPageView.as_view(),
        name="forgot_password",
    )

]