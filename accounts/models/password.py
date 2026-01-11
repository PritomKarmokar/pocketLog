import ulid
from typing import Optional
from datetime import timezone, timedelta

from django.db import models

from applibs.logger import get_logger

logger = get_logger(__name__)

class PasswordChangeRequestManager(models.Manager):
    def create_new_request(
        self,
        hashed_token: str,
        user_id: str,
    ) -> Optional["PasswordChangeRequest"]:
        try:
            created_at = timezone.now()
            valid_till = created_at + timedelta(minutes=30)

            request_object = self.create(
                hashed_token=hashed_token,
                user_id=user_id,
                created_at=created_at,
                valid_till=valid_till,
            )
            logger.info("Created new PasswordChangeRequest for user_id: %s", request_object.user_id)
            return request_object
        except Exception as e:
            logger.error("Error creating new PasswordChangeRequest: %s", str(e))
            return None


    def fetch_valid_request(
        self,
        hashed_token: str
    )-> Optional["PasswordChangeRequest"]:
        try:
            request_object = self.get(
                hashed_token=hashed_token,
                is_used=False,
            )
            current_time = timezone.now()
            if request_object and request_object.valid_till <= current_time:
                logger.info("Fetched valid PasswordChangeRequest for user_id: %s", request_object.user_id)
                return request_object
            
            return None
        except Exception as e:
            logger.error("Error fetching Password Change Request: %s", str(e))
            return None

class PasswordChangeRequest(models.Model):
    id = models.CharField(max_length=26, primary_key=True, editable=False)
    hashed_token = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    valid_till = models.DateTimeField(blank=True, null=True)
    is_used = models.BooleanField(default=False)

    objects = PasswordChangeRequestManager()

    def __str__(self) -> str:
        return f"PasswordChangeRequest(id={self.id}, user_id={self.user_id}, is_used={self.is_used})"
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(ulid.new())
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = "password_change_requests"
        verbose_name = "Password Change Request"
