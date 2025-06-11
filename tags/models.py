    # D:\django-job-portal-master\tags\models.py (Example if you want created_at/updated_at)

from django.db import models
from django.utils import timezone

class Tag(models.Model):
        name = models.CharField(max_length=50, unique=True)
        created_at = models.DateTimeField(auto_now_add=True) # Added for consistency
        updated_at = models.DateTimeField(auto_now=True) # Added for consistency

        class Meta:
            verbose_name = "Tag"
            verbose_name_plural = "Tags"
            ordering = ['name']

        def __str__(self):
            return self.name
    