    # D:\django-job-portal-master\jobsapp\models.py

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from .manager import JobManager 

from jobs.models import Company # IMPORTANT: Ensure Company model is imported from the 'jobs' app
from categories.models import Category # IMPORTANT: Ensure Category model is imported
from tags.models import Tag # IMPORTANT: Ensure Tag model is imported


class Job(models.Model):
        # These ForeignKeys are now non-nullable in the model definition
        company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
        
        title = models.CharField(max_length=300)
        location = models.CharField(max_length=150)
        salary = models.IntegerField(default=0, blank=True, null=True)
        description = models.TextField()
        
        category = models.ForeignKey(Category, on_delete=models.RESTRICT) # Non-nullable, restrict delete for integrity
        tags = models.ManyToManyField(Tag, blank=True) # Blank=True means it's not required in forms, but exists.

        job_type_choices = (
            ('1', 'Full time'),
            ('2', 'Part time'),
            ('3', 'Internship'),
        )
        type = models.CharField(max_length=10, choices=job_type_choices, default='1')

        vacancy = models.IntegerField(default=0)
        last_date = models.DateField()
        is_published = models.BooleanField(default=False)
        created_at = models.DateTimeField(auto_now_add=True)
        filled = models.BooleanField(default=False)
        user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

        objects = JobManager() 

        # --- @property DECORATORS for accessing Company data ---
        @property
        def company_name(self):
            return self.company.name if self.company else "N/A"

        @property
        def company_description(self):
            return self.company.description if self.company else "No description provided."

        @property
        def website(self):
            return self.company.website if self.company else "#"

        def get_absolute_url(self):
            return reverse('jobs:jobs-detail', kwargs={'id': self.id})

        def __str__(self):
            return self.title

class JobApplication(models.Model):
        job = models.ForeignKey(Job, on_delete=models.CASCADE)
        applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return self.applicant.email

class Applicant(models.Model):
        user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
        job = models.ForeignKey(Job, on_delete=models.CASCADE)
        created_at = models.DateTimeField(auto_now_add=True)

        class Meta:
            unique_together = ('user', 'job') # Ensure this unique constraint is defined if you need it

        def __str__(self):
            return self.user.email

class Favorite(models.Model):
        user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
        job = models.ForeignKey(Job, on_delete=models.CASCADE)
        soft_deleted = models.BooleanField(default=False)
        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return f"{self.user.email} favorited {self.job.title}"
    