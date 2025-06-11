    # D:\django-job-portal-master\jobsapp\urls.py

from django.urls import include, path

    # CONSOLIDATED IMPORTS FROM jobsapp.views
from .views import (
        HomeView, SearchView, JobListView, JobDetailsView, ApplyJobView, favorite,
        CompanyDetailView, add_review, AboutUsView, JobCreateView, JobUpdateView,
        DashboardView, ApplicantsListView, ApplicantPerJobView, AppliedApplicantView,
        filled, SendResponseView, EmployeeMyJobsListView, FavoriteListView
    )

app_name = "jobs" # This should already be 'jobs'

urlpatterns = [
        path("", HomeView.as_view(), name="home"),
        path("favorite/", favorite, name="favorite"),
        path("search/", SearchView.as_view(), name="search"),
        
        # Company Detail and Review URLs
        path('company/<int:pk>/', CompanyDetailView.as_view(), name='company_detail'),
        path('company/<int:company_id>/add_review/', add_review, name='add_review'),

        # Employer Dashboard and Job Management
        path(
            "employer/dashboard/",
            include(
                [
                    path("", DashboardView.as_view(), name="employer-dashboard"),
                    path("all-applicants/", ApplicantsListView.as_view(), name="employer-all-applicants"),
                    path("applicants/<int:job_id>/", ApplicantPerJobView.as_view(), name="employer-dashboard-applicants"),
                    path(
                        "applied-applicant/<int:job_id>/view/<int:applicant_id>",
                        AppliedApplicantView.as_view(),
                        name="applied-applicant-view",
                    ),
                    path("mark-filled/<int:job_id>/", filled, name="job-mark-filled"),
                    path("send-response/<int:applicant_id>", SendResponseView.as_view(), name="applicant-send-response"),
                    path("jobs/create/", JobCreateView.as_view(), name="employer-jobs-create"),
                    path("jobs/<int:id>/edit/", JobUpdateView.as_view(), name="employer-jobs-edit"),
                ]
            ),
        ),

        # Employee Specific Pages
        path(
            "employee/",
            include(
                [
                    path("my-applications", EmployeeMyJobsListView.as_view(), name="employee-my-applications"),
                    path("favorites", FavoriteListView.as_view(), name="employee-favorites"),
                ]
            ),
        ),

        # Job Application and Listing
        path("apply-job/<int:job_id>/", ApplyJobView.as_view(), name="apply-job"),
        path("jobs/", JobListView.as_view(), name="jobs"),
        path("jobs/<int:id>/", JobDetailsView.as_view(), name="jobs-detail"),
        path("about-us/", AboutUsView.as_view(), name="about-us"),
    ]
    