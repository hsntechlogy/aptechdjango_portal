# D:\django-job-portal-master\django_job_portal\urls.py

# THIS IS NOW YOUR PROJECT'S MAIN URLS.PY FILE (ROOT_URLCONF)

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.views.decorators.csrf import csrf_exempt
from graphene_file_upload.django import FileUploadGraphQLView

import os # CRITICAL FIX: Import the 'os' module here

# Import views directly from jobsapp.views (the monolithic file)
from jobsapp import views as jobsapp_views

# Schema view for Swagger/Redoc API documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Jobs Portal API",
        default_version="v1",
        description="Jobs Portal Api Description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Internationalization patterns: URLs that should be translated
lang_patterns = i18n_patterns(
    path("", include("jobsapp.urls", namespace="jobsapp")), # Main job-related app
    path("accounts/", include("accounts.urls")), # User accounts and auth
    path("notifications/", include("notifications.urls")), # User notifications
    path("categories/", include("categories.urls")), # Job categories
    path("tags/", include("tags.urls")), # Job tags
    path("resume-cv/", include("resume_cv.urls")), # Resume builder
)

# Main URL patterns (this will be the urlpatterns list for your entire project)
urlpatterns = lang_patterns + [
    re_path(r"^i18n/", include("django.conf.urls.i18n")),

    path("admin/", admin.site.urls),

    # API documentation and endpoints
    path(
        "api/",
        include(
            [
                path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
                path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
                path("accounts/", include("accounts.api.urls")),
                path("jobsapp/", include("jobsapp.api.urls")),
                path("tags/", include("tags.api.urls")),
                path("categories/", include("categories.api.urls")),
            ]
        ),
    ),
    path("social-auth/", include("social_django.urls", namespace="social")),
    
    # GraphQL endpoint (uncomment if you're using Graphene/GraphQL)
    # path("graphql/", csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True))),
    
]

# Assign custom error handlers - these MUST be at the top level of the ROOT_URLCONF
# They reference functions in jobsapp.views (the monolithic file)
handler400 = jobsapp_views.custom_bad_request_view
handler403 = jobsapp_views.custom_permission_denied_view
handler404 = jobsapp_views.custom_page_not_found_view
handler500 = jobsapp_views.custom_server_error_view

# Prometheus metrics (if ENABLE_PROMETHEUS is True in settings)
if hasattr(settings, 'ENABLE_PROMETHEUS') and settings.ENABLE_PROMETHEUS:
    urlpatterns.append(path("prometheus/", include("django_prometheus.urls")))

# Serve static and media files ONLY in development (DEBUG=True)
if settings.DEBUG:
    # Serve media files (user uploads)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Serve static files (CSS, JS, images) during development.
    # This combines STATIC_ROOT and STATICFILES_DIRS.
    # Note: STATIC_ROOT is primarily for collected static files for production.
    # For development, STATICFILES_DIRS and app-level static folders are typically used.
    # The line below ensures BASE_DIR/static is served.
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'static'))
    
    # If you also want to serve files from STATIC_ROOT during development
    # (e.g., if you're testing collectstatic output without running collectstatic locally)
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
