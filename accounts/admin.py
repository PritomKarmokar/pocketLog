from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ("username", "email", "is_staff", "is_active")
    list_filter = ("username", "email")
    ordering = ("email",)

    search_fields = (
        "email",
        "username",
    )
