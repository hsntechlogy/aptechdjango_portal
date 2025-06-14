# D:\django-job-portal-master\tags\urls.py

from django.urls import path
from . import views # Import views from the tags app (if you have any specific for tags)

app_name = "tags" # Define the app namespace here

urlpatterns = [
    # Example: If you had a view for listing all tags:
    # path('all/', views.TagListView.as_view(), name='tag-list'),
    # You can add specific tag-related URLs here.
    # For now, it can be empty or just contain this if no specific views are needed yet.
]

