# D:\django-job-portal-master\django_job_portal\settings.py

# ... (lines above) ...

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


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

    # Your apps - ENSURE 'jobs' is here and correctly spelled
    'accounts',
    'jobs',          # <<< CRITICAL: Ensure 'jobs' app is listed here and correctly spelled >>>
    'jobsapp',
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
    'tinymce',
    'django_cleanup.apps.CleanupConfig',
    'imagekit',
    'dal', 'dal_select2',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

ROOT_URLCONF = 'jobs.urls' # This was confirmed as your ROOT_URLCONF


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'notifications.context_processors.notifications_count',
            ],
            'libraries': {
                'is_already_applied': 'jobsapp.templatetags.is_already_applied',
                'jobsapp_tags': 'jobsapp.templatetags.jobsapp_tags',
                'humanize': 'django.contrib.humanize.templatetags.humanize',
            }
        },
    },
]

WSGI_APPLICATION = 'django_job_portal.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('en', 'English'),
    ('fr', 'Français'),
]
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]


STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    # BASE_DIR / 'static_dev',
]


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'mediafiles'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = 'accounts.CustomUser'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'webmaster@localhost'


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


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.linkedin.LinkedinOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
)


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
    'social_core.pipeline.social_data.get_user_send_response',
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
    'toolbar': 'undo redo | formatselect | bold italic backcolor | alignleft alignalignright alignjustify | bullist numlist outdent indent | removeformat | help',
    'custom_undo_redo_levels': 10,
    'selector': 'textarea',
}

# Add ALLOWED_HOSTS if DEBUG is False
DEBUG = False # Set to True during active development
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]'] # For local development
# When DEBUG is False, you must explicitly list your domain(s) here.
# E.g., ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

