from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, OTPVerification
from .forms import CustomUserCreationForm, CustomUserChangeForm

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
        add_form = CustomUserCreationForm
        form = CustomUserChangeForm

        list_display = (
            "email",
            "role",
            "is_active",
            "is_staff",
            "is_superuser",
            "is_company",
            "is_admin",
        )

        fieldsets = (
            (None, {"fields": ("email", "password")}),
            ("Personal info", {"fields": ("first_name", "last_name", "gender")}),
            ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions", "is_company", "is_admin", "role")}),
            ("Important dates", {"fields": ("last_login", "date_joined")}),
        )

        add_fieldsets = (
            (None, {"fields": ("email", "password", "password2")}),
            ("Personal info", {"fields": ("first_name", "last_name", "gender")}),
            ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions", "is_company", "is_admin", "role")}),
        )

        list_filter = (
            "is_active",
            "is_staff",
            "is_superuser",
            "is_company",
            "is_admin",
            "role",
        )
        search_fields = ("email", "role", "first_name", "last_name")
        ordering = ("email",)

@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
        list_display = ('user', 'otp_code', 'verified')
        search_fields = ('user__email',)
        list_filter = ('verified',)
        raw_id_fields = ('user',)
    