# D:\django-job-portal-master\django_job_portal\settings.py
# THIS IS YOUR MAIN PROJECT SETTINGS FILE

import os
from pathlib import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR is now D:\django-job-portal-master\ (the project root containing manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent 

# --- CORE DJANGO SETTINGS ---
SECRET_KEY = 'your-very-strong-unique-secret-key-here-REPLACE-ME' # IMPORTANT: Change this to a strong, unique secret key!
# You can generate one using: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

DEBUG = True # <<< IMPORTANT: Setting DEBUG to True for development >>>
ALLOWED_HOSTS = [] 

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.sitemaps',
    'django.contrib.humanize', # For intcomma and other filters

    # Your custom apps
    'accounts',
    'jobs',       # Your app containing Company and CompanyReview
    'jobsapp',    # Your main jobs application logic
    'categories',
    'tags',
    'notifications',
    'resume_cv',

    # Third-party apps
    'rest_framework',
    'drf_yasg',
    'social_django',
    'oauth2_provider',
    'django_prometheus',
    'graphene_django',
    'tinymce', # For rich text editor
    'django_cleanup.apps.CleanupConfig', # For automatic file cleanup
    'imagekit', # For image processing
    'dal', 'dal_select2', # For Django Autocomplete Light and Select2
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware', # For internationalization
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

# Root URL configuration for your project - CRITICAL for this setup
ROOT_URLCONF = 'jobs.urls' # This explicitly tells Django where your main URL patterns are (within the 'jobs' app)

# CRITICAL: WSGI_APPLICATION must point to the wsgi.py file within your project folder
# Assuming 'django_job_portal' is the name of your inner project folder (the one containing settings.py, urls.py, wsgi.py)
WSGI_APPLICATION = 'django_job_portal.wsgi.application' 

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Correctly points to D:\django-job-portal-master\templates
        'APP_DIRS': True, # Crucial for finding templates in app/templates folders (e.g., jobsapp/templates/jobsapp/)
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n', # Ensure this is here for i18n
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'notifications.context_processors.notifications_count', 
            ],
            'libraries': { 
                # Register your custom template tags under the app_name (jobsapp in this case)
                'jobsapp_tags': 'jobsapp.templatetags.jobsapp_tags', # This should contain both is_favorited and is_already_applied
                'humanize': 'django.contrib.humanize.templatetags.humanize',
            }
        },
    },
]


# Database configuration (example for MySQL)
DATABASES = {
      'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jobportal', 
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306', 
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization (i18n)
LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
LANGUAGES = [
    ('en', 'English'),
    ('fr', 'Français'),
]
LOCALE_PATHS = [
    BASE_DIR / 'locale', # Point to D:\django-job-portal-master\locale
]


STATIC_URL = '/static/'

# The directory where `collectstatic` will gather all static files for deployment.
# This should be outside of your app directories.
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Additional locations of static files for the development server.
# Django's `runserver` will look here IN ADDITION to static/ folders within apps.
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media files (user-uploaded content)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'mediafiles' # Correctly points to D:\django-job-portal-master\mediafiles

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model - CRITICAL
AUTH_USER_MODEL = 'accounts.CustomUser'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'  # <<< IMPORTANT: Replace with your actual email or use an environment variable >>>
EMAIL_HOST_PASSWORD = 'your_app_password_or_env_var' # <<< IMPORTANT: Use an app password if 2FA is on. NEVER hardcode in production. >>>

# Django REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# Django Authentication Backends (Crucial for custom user models and social auth)
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # Must be first for Django's admin and regular login
    'social_core.backends.linkedin.LinkedinOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
)

# Social Auth settings (replace with your actual keys)
# Best practice: load from environment variables
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('GOOGLE_OAUTH2_KEY', '')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('GOOGLE_OAUTH2_SECRET', '')
SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get('FACEBOOK_KEY', '')
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get('FACEBOOK_SECRET', '')
SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = os.environ.get('LINKEDIN_OAUTH2_KEY', '')
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = os.environ.get('LINKEDIN_OAUTH2_SECRET', '')

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_data.social_user',
    'social_core.pipeline.social_data.extract_username',
    'social_core.pipeline.mail.mail_validation',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_data.associate_user',
    # 'social_core.pipeline.social_data.get_user_send_response', # Removed this if not custom
    'social_core.pipeline.user.user_details',
)

SITE_ID = 1

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

ENABLE_PROMETHEUS = os.environ.get('ENABLE_PROMETHEUS', 'False').lower() in ('true', '1', 't')

TINYMCE_DEFAULT_CONFIG = {
    'height': 300,
    'menubar': False,
    'plugins': 'advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code fullscreen insertdatetime media table paste code help wordcount',
    'toolbar': 'undo redo | formatselect | bold italic backcolor | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | removeformat | help',
    'custom_undo_redo_levels': 10,
    'selector': 'textarea',
}
