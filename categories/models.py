# D:\django-job-portal-master\categories\models.py

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # CRITICAL FIX: Added null=True and blank=True to slug field
    slug = models.SlugField(unique=True, max_length=100, null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

