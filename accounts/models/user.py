import ulid
from typing import Any, Optional

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

from applibs.logger import get_logger
from applibs.choice import AuthProvider

logger = get_logger(__name__)

class UserManager(BaseUserManager):
    def create_user(
        self,
        email: str,
        password: str = None,
        **extra_fields: Any
    ) -> AbstractUser:
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        password: str,
        **extra_fields: Any
    ) -> AbstractUser:
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email=email, password=password, **extra_fields)

    def fetch_user_with_email(self, email: str) -> Optional[AbstractUser]:
        try:
            user = self.get(email=email)
            return user
        except self.model.DoesNotExist:
            return None

    def fetch_user_by_id(self, user_id: str) -> Optional[AbstractUser]:
        try:
            user = self.get(id=user_id)
            return user
        except self.model.DoesNotExist:
            return None


class User(AbstractUser):
    id = models.CharField(max_length=26, primary_key=True, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=55)
    date_joined = models.DateTimeField(default=timezone.now)
    auth_provider = models.CharField(
        max_length=10,
        choices=AuthProvider.choices,
        default=AuthProvider.Local
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self) -> str:
        return f"{self.username}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = ulid.new().__str__()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'User'
        db_table = 'users'

    @property
    def profile_response_data(self) -> dict:
        return {
            "username": self.username,
            "joining_date": self.date_joined.strftime("%d-%m-%Y %H:%M:%S")
        }

    def mark_logged_in(self) -> bool:
        self.last_login = timezone.now()
        self.save()
        return True

    def add_password(self, password: str) -> bool:
        self.set_password(password)
        self.save()
        return True