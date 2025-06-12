# D:\django-job-portal-master\categories\models.py

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, max_length=100) # Added slug for cleaner URLs
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories" # Correct plural name in admin

    def __str__(self):
        return self.name

