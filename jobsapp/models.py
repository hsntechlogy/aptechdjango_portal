# D:\django-job-portal-master\jobsapp\models.py

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from .manager import JobManager 

# IMPORTANT: Ensure Company model is imported from the 'jobs' app (your `jobs` app)
from jobs.models import Company 

# Import Category and Tag models from their respective apps
from categories.models import Category
from tags.models import Tag


class Job(models.Model):
    # Changed to models.ForeignKey(Company, ...)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    
    title = models.CharField(max_length=300)
    location = models.CharField(max_length=150)
    salary = models.IntegerField(default=0, blank=True, null=True)
    description = models.TextField()
    
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    tags = models.ManyToManyField(Tag, blank=True)

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

    apply_url = models.URLField(blank=True, null=True, help_text="Optional: URL where users can apply on an external site.")

    objects = JobManager() # Custom manager for Job model

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
        # Ensure this URL namespace matches your jobsapp.urls definition
        return reverse('jobsapp:jobs-detail', kwargs={'id': self.id}) 

    def __str__(self):
        return self.title


class Applicant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    
    cv = models.FileField(upload_to='applicant_cvs/', blank=True, null=True, 
                          help_text="Upload your resume/CV (PDF, DOCX).")
    
    STATUS_CHOICES = (
        (1, 'Pending'),
        (2, 'Accepted'),
        (3, 'Rejected'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    
    created_at = models.DateTimeField(auto_now_add=True)
    # Renamed to 'applied_at' for clarity
    applied_at = models.DateTimeField(auto_now_add=True) 


    class Meta:
        unique_together = ('user', 'job') # Prevents duplicate applications for the same job by the same user

    def __str__(self):
        return f"{self.user.email} applied for {self.job.title}"


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    soft_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} favorited {self.job.title}"

