# D:\django-job-portal-master\notifications\admin.py

from django.contrib import admin
from .models import Notification # Import the Notification model

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__email', 'message') # Search by user's email or message content
    raw_id_fields = ('user',) # Use raw ID input for ForeignKey to User

