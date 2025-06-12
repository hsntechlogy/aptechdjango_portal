# D:\django-job-portal-master\jobsapp\api\urls.py

from django.urls import path
from jobsapp.api.views.common import JobListCreateAPIView, JobRetrieveUpdateDestroyAPIView # Import API views

urlpatterns = [
    # API endpoints for jobs
    path('jobs/', JobListCreateAPIView.as_view(), name='api-job-list-create'),
    path('jobs/<int:id>/', JobRetrieveUpdateDestroyAPIView.as_view(), name='api-job-detail'),
    
    # You can add more API endpoints here for other models (e.g., Applicants, Favorites)
    # path('applicants/', ApplicantListCreateAPIView.as_view(), name='api-applicant-list-create'),
    # path('applicants/<int:id>/', ApplicantRetrieveUpdateDestroyAPIView.as_view(), name='api-applicant-detail'),
    # path('favorites/', FavoriteListCreateAPIView.as_view(), name='api-favorite-list-create'),
]
