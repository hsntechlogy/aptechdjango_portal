# D:\django-job-portal-master\accounts\urls.py

# Removed unnecessary settings and static imports as they belong in project's main urls.py
from django.urls import path, include

# Import specific class-based views from the current app (accounts.views)
from .views import RegisterEmployeeView, RegisterEmployerView, LoginView, LogoutView

# Import function-based views from the current app (accounts.views)
from . import views 

# Import views from jobsapp for profile updates (keeping your current structure)
from accounts.views import EditProfileView, EmployerProfileEditView # Assuming these are defined in jobsapp/views.py

app_name = "accounts"

urlpatterns = [
    # Existing registration views
    path("employee/register/", RegisterEmployeeView.as_view(), name="employee-register"),
    path("employer/register/", RegisterEmployerView.as_view(), name="employer-register"),

    # Profile update views (from jobsapp, but defined in accounts URLs as per your current setup)
    path("employee/profile/update/", EditProfileView.as_view(), name="employee-profile-update"),
    path("employer/profile/update/", EmployerProfileEditView.as_view(), name="employer-profile-update"),

    # Authentication views
    path("logout/", LogoutView.as_view(), name="logout"),
    path("login/", LoginView.as_view(), name="login"),

    # OTP Verification URLs
    path('verify-otp/<int:user_id>/', views.verify_otp, name='verify_otp_page'),
    path('resend-otp/<int:user_id>/', views.resend_otp, name='resend_otp'),

    # Admin dashboard view
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # <<< FIX: Removed the duplicate notification URL here >>>
    # The 'notifications/' URL inclusion should only happen once in the project's main urls.py
    # and the specific 'notifications' view should be handled there if needed,
    # or within the notifications app's urls.py if it's part of that app's patterns.
]

# <<< FIX: Removed static files serving from here - it belongs in the project's main urls.py >>>
# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
