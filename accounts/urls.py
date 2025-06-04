from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from jobsapp.views import EditProfileView, EmployerProfileEditView
from .views import *

app_name = "accounts"

urlpatterns = [
    path("employee/register/", RegisterEmployeeView.as_view(), name="employee-register"),
    path("employer/register/", RegisterEmployerView.as_view(), name="employer-register"),
    path("employee/profile/update/", EditProfileView.as_view(), name="employee-profile-update"),
    path("employer/profile/update/", EmployerProfileEditView.as_view(), name="employer-profile-update"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("login/", LoginView.as_view(), name="login"),
<<<<<<< HEAD
] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
=======
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> 22a1e464de6d88d694fc8d7e62562c2666c47c6b
