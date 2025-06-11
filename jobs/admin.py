from django.contrib import admin
from .models import Company, CompanyReview # Import the Company models

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
        list_display = ('name', 'user', 'website', 'created_at')
        search_fields = ('name', 'user__email')
        list_filter = ('created_at',)
        raw_id_fields = ('user',)

@admin.register(CompanyReview)
class CompanyReviewAdmin(admin.ModelAdmin):
        list_display = ('company', 'user', 'rating', 'created_at')
        search_fields = ('company__name', 'user__email', 'comment')
        list_filter = ('rating', 'created_at')
        raw_id_fields = ('company', 'user',)
    