# D:\django-job-portal-master\jobsapp\urls.py

from django.urls import path, include
from . import views # Import all views from the monolithic jobsapp.views

app_name = "jobsapp" # Define the app namespace here

urlpatterns = [
    # Public-facing views
    path("", views.HomeView.as_view(), name="home"),
    path("about-us/", views.AboutUsView.as_view(), name="about-us"),
    path("jobs/", views.JobListView.as_view(), name="jobs"),
    path("jobs/<int:id>/", views.JobDetailsView.as_view(), name="jobs-detail"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("apply-job/<int:job_id>/", views.ApplyJobView.as_view(), name="apply-job"),
    path("favorite/", views.favorite, name="favorite"),
    path("company/<int:pk>/", views.CompanyDetailView.as_view(), name="company_detail"), 
    
    # Review functionality (if in jobsapp.views)
    path('company/<int:company_id>/add_review/', views.add_review, name='add_review'),

    # Employee-specific views
    path("employee/my-applications/", views.EmployeeMyJobsListView.as_view(), name="employee-my-applications"),
    path("employee/favorites/", views.FavoriteListView.as_view(), name="employee-favorites"),
    # Note: EmployeeProfileEditView is now in accounts.urls.py, not here.

    # Employer-specific views
    path("employer/dashboard/", views.DashboardView.as_view(), name="employer-dashboard"),
    path("employer/dashboard/jobs/create/", views.JobCreateView.as_view(), name="employer-job-create"),
    path("employer/dashboard/jobs/update/<int:id>/", views.JobUpdateView.as_view(), name="employer-job-update"),
    path("employer/dashboard/applicants/", views.ApplicantsListView.as_view(), name="employer-dashboard-applicants-all"),
    path("employer/dashboard/applicants/<int:job_id>/", views.ApplicantPerJobView.as_view(), name="employer-dashboard-applicants"),
    path("employer/dashboard/applicants/<int:job_id>/<int:applicant_id>/", views.AppliedApplicantView.as_view(), name="applied-applicant-view"),
    path("employer/dashboard/applicants/<int:job_id>/<int:applicant_id>/send-response/", views.SendResponseView.as_view(), name="applicant-send-response"),
    path("employer/job/filled/<int:job_id>/", views.filled, name="job-filled"),
    # Note: EmployerProfileEditView is now in accounts.urls.py, not here.

]

