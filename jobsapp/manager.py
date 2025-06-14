# D:\django-job-portal-master\jobsapp\manager.py

from django.db import models

class JobManager(models.Manager):
    def unfilled_jobs(self):
        """Returns jobs that are not yet filled."""
        return self.filter(filled=False)

    def published_jobs(self):
        """Returns jobs that are published."""
        return self.filter(is_published=True)

    def active_jobs(self):
        """Returns jobs that are both published and not filled."""
        return self.published_jobs().unfilled_jobs()

    def get_queryset(self):
        # Override the default queryset to include a default ordering if desired
        # or other common filters. For now, just call super().get_queryset()
        return super().get_queryset()

