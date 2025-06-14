# D:\django-job-portal-master\accounts\models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager # Import BaseUserManager
from django.utils.translation import gettext_lazy as _

# Define a custom User Manager for CustomUser
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a regular user with the given email and password.
        Email is used as the primary identifier.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        Superusers are always active, staff, superuser, and have an 'admin' role.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'admin') # Set role to admin for superuser

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

# Custom User Model definition
class CustomUser(AbstractUser):
    # Use our custom manager for this model
    objects = CustomUserManager() 

    # We allow the default 'username' field to be blank and null.
    # The 'email' field will be the USERNAME_FIELD for authentication.
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    
    # Email field is unique and will be used for login
    email = models.EmailField(_('email address'), unique=True)

    # GENDER_CHOICES and gender field
    GENDER_CHOICES = (
        ('male', _('Male')),
        ('female', _('Female')),
        ('other', _('Other')),
        ('prefer_not_to_say', _('Prefer not to say')),
    )
    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
        verbose_name=_('Gender')
    )

    # ROLE_CHOICES and role field
    ROLE_CHOICES = (
        ('employee', 'Employee'),
        ('employer', 'Employer'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')

    # Additional flags
    is_company = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    # Define email as the USERNAME_FIELD for authentication
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS are fields prompted when creating a user via createsuperuser
    # 'username' is explicitly removed here as email is the USERNAME_FIELD
    REQUIRED_FIELDS = ['first_name', 'last_name'] 

    def __str__(self):
        return self.email 

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

# OTPVerification Model
class OTPVerification(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='otp_code_verification')
    otp_code = models.CharField(max_length=6)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"OTP for {self.user.email}: {self.otp_code} (Verified: {self.verified})"

