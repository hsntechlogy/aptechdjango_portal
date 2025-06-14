# D:\django-job-portal-master\resume_cv\urls.py

from django.urls import path
from . import views
from .views import UserResumeListView, ResumeCVCreateView, download_resume

app_name = "resume_cv"

urlpatterns = [
    # --- RESUME BUILDER AND TEMPLATE RELATED URLs REMOVED ---
    # path('templates/', views.TemplateListView.as_view(), name='templates'), # Removed
    # path('builder/<str:code>/', views.resume_builder, name='builder'), # Removed
    # path('update/<int:id>/', views.update_builder, name='update'), # Removed
    # path('load/<int:id>/', views.load_builder, name='load'), # Removed
    # path('update_template_choice/<int:id>/', views.update_template_choice, name='update_template_choice'), # Removed

    # --- KEEPING ONLY ESSENTIAL RESUME MANAGEMENT (e.g., for uploaded resumes) ---
    path('resumes/', UserResumeListView.as_view(), name='resumes'),
    path('create/', ResumeCVCreateView.as_view(), name='create_resume'), # Assuming this is for general resume creation/upload
    path('download/<int:id>/', download_resume, name='download_resume'),
]
