    # D:\django-job-portal-master\notifications\models.py

from django.db import models
from django.conf import settings # Import settings to use AUTH_USER_MODEL

class Notification(models.Model):
        user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name='notifications_received' # Corrected related_name
        )
        message = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)
        is_read = models.BooleanField(default=False)

        def __str__(self):
            return f"Notification for {self.user.email}: {self.message[:50]}"
    