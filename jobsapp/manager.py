# D:\django-job-portal-master\jobsapp\manager.py

from django.db import models

class JobManager(models.Manager):
    """
    Custom manager for the Job model to provide specific querysets.
    """
    def unfilled_jobs(self):
        """Returns only jobs that are not yet filled."""
        return self.filter(filled=False)

    def published_jobs(self):
        """Returns only jobs that are published."""
        return self.filter(is_published=True)

    def active_jobs(self):
        """Returns jobs that are published and not filled."""
        return self.published_jobs().filter(filled=False)

