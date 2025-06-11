    # D:\django-job-portal-master\jobsapp\admin.py

from django.contrib import admin
from .models import Job, Applicant, Favorite 
from categories.models import Category # IMPORTANT: Ensure Category model is imported
from tags.models import Tag # IMPORTANT: Ensure Tag model is imported
from jobs.models import Company # IMPORTANT: Ensure Company model is imported


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
        list_display = (
            'title', 
            'company', 
            'location', 
            'type', 
            'category', 
            'is_published', 
            'created_at',
            'filled',
        )
        list_filter = ('type', 'is_published', 'filled', 'category', 'created_at')
        search_fields = ('title', 'location', 'description', 'company__name')
        raw_id_fields = ('user', 'company', 'category') # Add category to raw_id_fields for easier selection
        filter_horizontal = ('tags',) # For ManyToManyField

        fieldsets = (
            (None, {'fields': ('user', 'company', 'title', 'description', 'location', 'type', 'category', 'tags')}),
            ('Job Details', {'fields': ('salary', 'vacancy', 'last_date', 'is_published', 'filled')}),
        )

@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
        list_display = ('user', 'job', 'created_at')
        search_fields = ('user__email', 'job__title')
        raw_id_fields = ('user', 'job')

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
        list_display = ('user', 'job', 'soft_deleted', 'created_at')
        list_filter = ('soft_deleted', 'created_at')
        search_fields = ('user__email', 'job__title')
        raw_id_fields = ('user', 'job')
    