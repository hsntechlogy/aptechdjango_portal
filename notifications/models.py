# D:\django-job-portal-master\notifications\models.py
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_notifications', verbose_name=_("User"))
    message = models.TextField(verbose_name=_("Message"))
    is_read = models.BooleanField(default=False, verbose_name=_("Is Read"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
        ordering = ['-created_at'] # Order by newest first

    def __str__(self):
        return f"Notification for {self.user.email}: {self.message[:50]}..."

    def mark_as_read(self):
        self.is_read = True
        self.save()