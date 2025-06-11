 # D:\django-job-portal-master\tags\admin.py

from django.contrib import admin
from .models import Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
        list_display = ('name', 'created_at', 'updated_at')
        search_fields = ('name',)
        list_filter = ('created_at',)
    