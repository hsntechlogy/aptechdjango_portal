from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

# Import specific class-based views from the current app (accounts.views)
from .views import RegisterEmployeeView, RegisterEmployerView, LoginView, LogoutView
# Import specific function-based views from the current app (accounts.views)
# The `send_otp_email` and `request_otp` helpers are not directly in URLs,
# but `verify_otp` and `resend_otp` are.
from . import views # Keep this for direct function views like verify_otp, resend_otp, admin_dashboard, notifications

# Import views from other apps for profile updates
from jobsapp.views import EditProfileView, EmployerProfileEditView

app_name = "accounts"

urlpatterns = [
    # Existing registration views (assuming OTP generation/redirect handled in their post methods)
    path("employee/register/", RegisterEmployeeView.as_view(), name="employee-register"),
    path("employer/register/", RegisterEmployerView.as_view(), name="employer-register"),

    # Profile update views (from jobsapp)
    path("employee/profile/update/", EditProfileView.as_view(), name="employee-profile-update"),
    path("employer/profile/update/", EmployerProfileEditView.as_view(), name="employer-profile-update"),

    # Authentication views
    path("logout/", LogoutView.as_view(), name="logout"),
    path("login/", LoginView.as_view(), name="login"),

    # --- OTP Verification URLs (UPDATED) ---
    # This URL now takes the user_id to verify a specific user's OTP
    path('verify-otp/<int:user_id>/', views.verify_otp, name='verify_otp_page'),
    # This URL allows a user to request a new OTP if needed
    path('resend-otp/<int:user_id>/', views.resend_otp, name='resend_otp'),

    # Admin dashboard and notifications views
    # Removed duplicate 'admin-dashboard/' entry
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('notifications/', views.notifications, name='notifications'),
] 

if settings.DEBUG:
    # This static files configuration typically goes in your project's main urls.py (e.g., job_portal/urls.py)
    # However, if it's explicitly here and you need it, ensure STATICFILES_DIRS[0] is valid.
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

