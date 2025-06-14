# D:\django-job-portal-master\accounts\admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import CustomUser, OTPVerification 
from .forms import CustomUserCreationForm, CustomUserChangeForm 


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    list_display = ('email', 'first_name', 'last_name', 'role', 'gender', 'is_active', 'is_staff', 'is_superuser',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}), 
        ('Personal info', {'fields': ('first_name', 'last_name', 'gender')}), 
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Roles', {'fields': ('role', 'is_company', 'is_admin')}), 
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2') 
        }),
        ('Personal info', {'fields': ('first_name', 'last_name', 'gender')}),
        ('Roles', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'is_company', 'is_admin')}),
    )
    
    search_fields = ('email', 'first_name', 'last_name', 'role',) 
    ordering = ('email',) 

    filter_horizontal = ('groups', 'user_permissions',)


@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp_code', 'verified', 'created_at')
    list_filter = ('verified', 'created_at',) 
    search_fields = ('user__email', 'otp_code',) 

