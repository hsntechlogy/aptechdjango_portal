# D:\django-job-portal-master\accounts\api\urls.py

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# You would define your custom API views for accounts here
# from .views import UserRegistrationAPIView, UserProfileAPIView, etc.

urlpatterns = [
    # JWT authentication endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Add your custom user-related API endpoints here, e.g.:
    # path('register/', UserRegistrationAPIView.as_view(), name='api-register'),
    # path('profile/', UserProfileAPIView.as_view(), name='api-profile'),
]

