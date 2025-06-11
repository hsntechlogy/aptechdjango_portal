    # D:\django-job-portal-master\categories\models.py

from django.db import models
from django.utils import timezone # Make sure this is imported!

class Category(models.Model):
        name = models.CharField(max_length=100, unique=True)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        class Meta:
            verbose_name = "Category"
            verbose_name_plural = "Categories"
            ordering = ['name']

        def __str__(self):
            return self.name
    