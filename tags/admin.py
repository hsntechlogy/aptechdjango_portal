# D:\django-job-portal-master\tags\admin.py

from django.contrib import admin
from .models import Tag # Import the Tag model

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at') # Display slug in list view
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)} # Automatically populate slug from name

