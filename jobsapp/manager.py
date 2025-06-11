    # D:\django-job-portal-master\jobsapp\manager.py

from django.db import models
from model_utils.managers import InheritanceManager


class JobManager(InheritanceManager):
        # Modified to accept and pass through arbitrary keyword arguments for filtering
        def unfilled(self, **kwargs):
            # Apply filled=False filter and then any additional kwargs received
            return self.filter(filled=False, **kwargs)

    