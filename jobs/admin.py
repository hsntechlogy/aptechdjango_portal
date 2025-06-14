# D:\django-job-portal-master\jobs\admin.py

from django.contrib import admin
from .models import Company, CompanyReview # Import Company and CompanyReview models

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'website', 'created_at')
    search_fields = ('name', 'user__email')
    raw_id_fields = ('user',)

@admin.register(CompanyReview)
class CompanyReviewAdmin(admin.ModelAdmin):
    list_display = ('company', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('company__name', 'user__email', 'comment')
    raw_id_fields = ('company', 'user')

