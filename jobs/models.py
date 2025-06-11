    # D:\django-job-portal-master\jobs\models.py

from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone

CustomUser = get_user_model()

class Company(models.Model):
        # Company.user should be non-nullable
        user = models.OneToOneField(
            CustomUser,
            on_delete=models.CASCADE,
            related_name='company_profile',
            limit_choices_to={'is_company': True},
            # null=False and blank=False are defaults, so no need to specify them.
        )
        name = models.CharField(max_length=255)
        description = models.TextField(blank=True, null=True)
        website = models.URLField(blank=True, null=True)
        logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
        
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return self.name

class CompanyReview(models.Model):
        company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='reviews')
        user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
        rating = models.IntegerField()
        comment = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return f"Review for {self.company.name} by {self.user.email}"
    