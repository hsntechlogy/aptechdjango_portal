# D:\django-job-portal-master\accounts\models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from accounts.managers import UserManager
from django.conf import settings

GENDER_CHOICES = [
    ("male", "Male"),
    ("female", "Female"),
    ("other", "Other"),
]

class CustomUser(AbstractUser): # Renamed from 'User' to 'CustomUser' as per your decision
    username = None # Remove the default username field

    role = models.CharField(
        max_length=12,
        error_messages={"required": "Role must be provided"}
    )
    gender = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        default="",
        choices=GENDER_CHOICES
    )
    email = models.EmailField(
        unique=True,
        blank=False,
        error_messages={"unique": "A user with that email already exists."}
    )

    is_company = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    # --- IMPORTANT: Set is_active to False by default ---
    is_active = models.BooleanField(default=False) # User is inactive until OTP verified

    REQUIRED_FIELDS = ['role']
    USERNAME_FIELD = "email"

    objects = UserManager()

    class Meta:
        verbose_name = "CustomUser"
        verbose_name_plural = "CustomUsers"

    def __str__(self):
        return self.email

# OTPVerification model (assuming this is correct and unique)
class OTPVerification(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"OTP for {self.user.email}" if self.user else "OTP Verification (User N/A)"