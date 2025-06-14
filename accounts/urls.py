# D:\django-job-portal-master\accounts\urls.py

from django.urls import path
from . import views # Import views from the accounts app

app_name = "accounts" # Define the app namespace

urlpatterns = [
    path('register/employee/', views.RegisterEmployeeView.as_view(), name='register-employee'),
    path('register/employer/', views.RegisterEmployerView.as_view(), name='register-employer'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    # OTP Verification
    path('verify-otp/<int:user_id>/', views.verify_otp, name='verify_otp_page'),
    path('resend-otp/<int:user_id>/', views.resend_otp, name='resend_otp'),

    # Profile Management
    path('employee/profile/<int:pk>/', views.EditProfileView.as_view(), name='employee-profile-update'),
    path('employer/profile/<int:pk>/', views.EmployerProfileEditView.as_view(), name='employer-profile-update'),

    # Admin Dashboard (if still used)
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    # path('notifications/', views.notifications, name='notifications'), # <<< CRITICAL FIX: REMOVED THIS LINE >>>
]
