# D:\django-job-portal-master\tags\models.py

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from django.conf import settings # Import settings to reference AUTH_USER_MODEL

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_("Tag Name"))
    slug = models.SlugField(unique=True, max_length=60, blank=True)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

# Assuming this Notification model exists in your tags app and is causing the clash
class Notification(models.Model):
    # CRITICAL FIX: Added related_name='tag_notifications'
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tag_notifications', verbose_name=_("User"))
    message = models.TextField(verbose_name=_("Message"))
    is_read = models.BooleanField(default=False, verbose_name=_("Is Read"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    class Meta:
        verbose_name = _("Tag Notification")
        verbose_name_plural = _("Tag Notifications")
        ordering = ['-created_at']

    def __str__(self):
        return f"Tag Notification for {self.user.email}: {self.message[:50]}..."

    def mark_as_read(self):
        self.is_read = True
        self.save()
