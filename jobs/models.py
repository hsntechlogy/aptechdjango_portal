# D:\django-job-portal-master\jobs\models.py

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Company(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employer_profile')
    name = models.CharField(max_length=255, verbose_name=_("Company Name"))
    description = models.TextField(verbose_name=_("Company Description"), blank=True, null=True)
    website = models.URLField(max_length=200, blank=True, null=True, verbose_name=_("Website"))
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True, verbose_name=_("Company Logo"))
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Address"))
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Phone Number"))
    email = models.EmailField(blank=True, null=True, verbose_name=_("Email"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")

    def __str__(self):
        return self.name

class CompanyReview(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name=_("Rating (1-5)"))
    comment = models.TextField(verbose_name=_("Comment"), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('company', 'user') # One review per user per company
        verbose_name = _("Company Review")
        verbose_name_plural = _("Company Reviews")
        ordering = ['-created_at']

    def __str__(self):
        return f"Review for {self.company.name} by {self.user.email} - Rating: {self.rating}"
