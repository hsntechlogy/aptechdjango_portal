    # D:\django-job-portal-master\notifications\urls.py

from django.urls import path
from . import views

app_name = "notifications" # Define the app_name for this app

urlpatterns = [
        path('notifications/', views.employee_notifications, name='employee_notifications'),
        path('notifications/create/', views.create_notification_for_employees, name='create_notification'),
        # Add any other notification-related URLs here
    ]
    