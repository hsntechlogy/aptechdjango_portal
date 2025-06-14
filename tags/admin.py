# D:\django-job-portal-master\tags\admin.py

from django.contrib import admin
from .models import Tag, Notification # Import both Tag and Notification from models.py

# Register your models here.

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

# Register the Notification model from tags.models.py
@admin.register(Notification)
class TagsNotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__email', 'message')

