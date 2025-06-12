# D:\django-job-portal-master\notifications\models.py

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Notification(models.Model):
    # Link to the user who receives the notification
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at'] # Order by newest first

    def __str__(self):
        return f"Notification for {self.user.email}: {self.message[:50]}..."

