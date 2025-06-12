# D:\django-job-portal-master\accounts\admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import CustomUser, OTPVerification 
from .forms import CustomUserCreationForm, CustomUserChangeForm # Import custom admin forms


# Register your CustomUser model with the admin site
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Use custom forms for adding/changing users in the admin
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    # Display email as the primary identifier in the list view, along with other custom fields
    list_display = ('email', 'first_name', 'last_name', 'role', 'gender', 'is_active', 'is_staff', 'is_superuser',)
    
    # Custom fieldsets for displaying user details in the admin form
    fieldsets = (
        (None, {'fields': ('email', 'password')}), # Email as primary identifier, password for changes
        ('Personal info', {'fields': ('first_name', 'last_name', 'gender')}), # Added gender
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Roles', {'fields': ('role', 'is_company', 'is_admin')}), # Assuming is_company and is_admin exist on CustomUser
    )
    # Custom fieldsets for adding new users in admin (ensuring all required fields are present)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2') # Email, password, and password confirmation
        }),
        ('Personal info', {'fields': ('first_name', 'last_name', 'gender')}),
        ('Roles', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'is_company', 'is_admin')}),
    )
    
    search_fields = ('email', 'first_name', 'last_name', 'role',) 
    ordering = ('email',) 

    filter_horizontal = ('groups', 'user_permissions',)


# Register the OTPVerification model for admin management
@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp_code', 'verified', 'created_at') 
    list_filter = ('verified', 'created_at',) 
    search_fields = ('user__email', 'otp_code',) 

