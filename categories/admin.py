# D:\django-job-portal-master\tags\models.py

from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, max_length=50) # Added slug for cleaner URLs
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

