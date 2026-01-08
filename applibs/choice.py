from django.db import models
from django.utils.translation import gettext_lazy as _

class AuthProvider(models.TextChoices):
    Local = 'local', _('Local')
    Google = 'google', _('Google')
