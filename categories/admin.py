    # D:\django-job-portal-master\categories\admin.py

from django.contrib import admin
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
        list_display = ('name', 'created_at', 'updated_at')
        search_fields = ('name',)
        list_filter = ('created_at',)

    