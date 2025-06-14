# D:\django-job-portal-master\django_job_portal\wsgi.py

import os

from django.core.wsgi import get_wsgi_application

# CRITICAL: This line tells Django where your settings file is located.
# Ensure 'django_job_portal.settings' matches your project structure.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_job_portal.settings')

application = get_wsgi_application()

