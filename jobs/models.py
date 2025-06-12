# D:\django-job-portal-master\jobs\models.py
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Assuming CustomUser is in the 'accounts' app and is your AUTH_USER_MODEL
# from accounts.models import CustomUser 
# It's better to use settings.AUTH_USER_MODEL directly if it's set in settings.py

class Company(models.Model):
    # Link Company to the employer user (CustomUser)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='company_profile')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"
        # Ensure only one company per user
        unique_together = ('user',) 

class CompanyReview(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)]) # 1-5 rating
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('company', 'user') # One review per user per company

    def __str__(self):
        return f"Review for {self.company.name} by {self.user.email}"

