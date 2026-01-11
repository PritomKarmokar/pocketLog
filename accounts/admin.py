from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User, PasswordChangeRequest

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    # Fields shown when creating a user
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username",
                "email",
                "password1",
                "password2",
                "is_staff",
                "is_superuser",
                "is_active",
            ),
        }),
    )
    fieldsets = UserAdmin.fieldsets + (
        ("Authentication", {"fields": ("auth_provider",)}),
    )
    list_display = ("username", "email", "is_staff", "is_active")
    ordering = ("email",)

    search_fields = (
        "email",
        "username",
    )

@admin.register(PasswordChangeRequest)
class PasswordChangeRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_id",
        "valid_till",
    )
    ordering = ("-created_at",)
    search_fields = ("user_id",)