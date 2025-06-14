# D:\django-job-portal-master\jobsapp\api\urls.py

from django.urls import path
from jobsapp.api.views.common import JobListCreateAPIView, JobRetrieveUpdateDestroyAPIView # Import API views

urlpatterns = [
    path('jobs/', JobListCreateAPIView.as_view(), name='api-job-list-create'),
    path('jobs/<int:id>/', JobRetrieveUpdateDestroyAPIView.as_view(), name='api-job-detail'),
]

