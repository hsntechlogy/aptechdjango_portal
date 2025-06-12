# D:\django-job-portal-master\jobs\admin.py

from django.contrib import admin
from .models import Company, CompanyReview # Import models from the 'jobs' app

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'website', 'created_at', 'updated_at')
    search_fields = ('name', 'user__email') # Search by company name or associated user's email
    list_filter = ('created_at',)
    # Automatically set the user if creating from admin, or ensure it's selectable
    raw_id_fields = ('user',) # Use a raw ID input for ForeignKey to User for large number of users

@admin.register(CompanyReview)
class CompanyReviewAdmin(admin.ModelAdmin):
    list_display = ('company', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('company__name', 'user__email', 'comment')
    raw_id_fields = ('company', 'user') # Use raw ID input for ForeignKeys
