# D:\django-job-portal-master\jobsapp\admin.py

from django.contrib import admin
from .models import Job, Applicant, Favorite # Import models from jobsapp

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'user', 'category', 'job_type', 'vacancy', 'last_date', 'is_published', 'filled', 'created_at')
    list_filter = ('is_published', 'filled', 'job_type', 'category', 'created_at')
    search_fields = ('title', 'location', 'company__name', 'user__email') # Search by job title, location, company name, or user email
    raw_id_fields = ('company', 'user') # Use raw ID input for ForeignKeys to Company and User
    filter_horizontal = ('tags',) # For ManyToMany field 'tags'
    date_hierarchy = 'created_at' # Add a date drill-down navigation
    
    # Custom actions
    actions = ['make_published', 'make_unpublished', 'mark_as_filled', 'mark_as_unfilled']

    def make_published(self, request, queryset):
        queryset.update(is_published=True)
        self.message_user(request, f"{queryset.count()} jobs marked as published.")
    make_published.short_description = "Mark selected jobs as published"

    def make_unpublished(self, request, queryset):
        queryset.update(is_published=False)
        self.message_user(request, f"{queryset.count()} jobs marked as unpublished.")
    make_unpublished.short_description = "Mark selected jobs as unpublished"

    def mark_as_filled(self, request, queryset):
        queryset.update(filled=True)
        self.message_user(request, f"{queryset.count()} jobs marked as filled.")
    mark_as_filled.short_description = "Mark selected jobs as filled"

    def mark_as_unfilled(self, request, queryset):
        queryset.update(filled=False)
        self.message_user(request, f"{queryset.count()} jobs marked as unfilled.")
    mark_as_unfilled.short_description = "Mark selected jobs as unfilled"


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'status', 'cv', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('user__email', 'job__title') # Search by applicant's email or job title
    raw_id_fields = ('user', 'job') # Use raw ID input for ForeignKeys

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'soft_deleted', 'created_at')
    list_filter = ('soft_deleted', 'created_at')
    search_fields = ('user__email', 'job__title') # Search by user's email or job title
    raw_id_fields = ('user', 'job') # Use raw ID input for ForeignKeys
