# D:\django-job-portal-master\jobsapp\urls.py

from django.urls import path
from . import views # Import views from the current app
from django.utils.translation import gettext_lazy as _

app_name = "jobsapp" # Define the namespace for this app

urlpatterns = [
    # General Job Listings and Search
    path("", views.HomeView.as_view(), name="home"),
    path("jobs/", views.JobListView.as_view(), name="jobs"),
    path("jobs/<int:id>/", views.JobDetailsView.as_view(), name="jobs-detail"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("about-us/", views.AboutUsView.as_view(), name="about-us"),

    # Employee Specific Paths
    path("employee/my-applications/", views.EmployeeMyApplicationsView.as_view(), name="employee-my-applications"),
    path("employee/favorites/", views.FavoriteListView.as_view(), name="employee-favorites"),
    path("jobs/<int:job_id>/apply/", views.ApplyJobView.as_view(), name="apply-job"),
    path("favorite/", views.favorite, name="favorite"), # AJAX endpoint for favorite toggling

    # Employer Specific Paths
    path("employer/dashboard/", views.DashboardView.as_view(), name="employer-dashboard"),
    path("employer/dashboard/applicants/", views.ApplicantsListView.as_view(), name="employer-dashboard-applicants-all"), # All applicants
    path("employer/dashboard/applicants/<int:job_id>/", views.ApplicantPerJobView.as_view(), name="employer-dashboard-applicants"), # Applicants for a specific job
    path("employer/dashboard/applicants/<int:job_id>/<int:applicant_id>/view/", views.AppliedApplicantView.as_view(), name="applied-applicant-view"),
    path("employer/dashboard/jobs/create/", views.JobCreateView.as_view(), name="employer-job-create"),
    path("employer/dashboard/jobs/<int:id>/update/", views.JobUpdateView.as_view(), name="employer-job-update"),
    path("employer/dashboard/jobs/<int:job_id>/filled/", views.job_filled_view, name="job-filled"),
    path("employer/dashboard/applicants/<int:applicant_id>/send-response/", views.SendResponseView.as_view(), name="send-response"),

    # Company & Review Paths 
    path('company/<int:pk>/', views.CompanyDetailView.as_view(), name='company_detail'),
    path('company/<int:company_id>/add_review/', views.add_review, name='add_review'),

]
