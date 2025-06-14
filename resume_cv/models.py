# D:\django-job-portal-master\resume_cv\models.py

from time import strftime

from django.db import models
import uuid

from accounts.models import CustomUser 
from utils.filename import generate_file_name 


def resume_cv_directory_path(instance, filename):
    """
    Defines the upload path for resume-related files (thumbnails, uploaded resumes).
    Files will be organized by year/month/day.
    """
    return "resumes/{0}/{1}".format(strftime("%Y/%m/%d"), generate_file_name() + "." + filename.split(".")[-1])


class ResumeCvCategory(models.Model):
    """
    Represents categories for resume templates.
    Kept for potential future use or historical data, but not actively used by the current upload-only flow.
    """
    name = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to=resume_cv_directory_path, blank=True, null=True)
    color = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ResumeCvTemplate(models.Model):
    """
    Represents pre-defined resume templates (HTML/CSS content).
    Kept for potential future use or historical data, but not actively used by the current upload-only flow.
    """
    category = models.ForeignKey(ResumeCvCategory, on_delete=models.CASCADE, related_name="templates")
    name = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to=resume_cv_directory_path, blank=True, null=True)
    content = models.TextField(null=True, blank=True) # HTML content of the template
    style = models.TextField(null=True, blank=True)   # CSS style of the template
    active = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ResumeCv(models.Model):
    """
    Represents a user's resume, now supporting direct file uploads.
    The 'template', 'content', and 'style' fields are made optional (nullable)
    to accommodate resumes uploaded as files without using the builder.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="resume_cvs")
    
    # Make 'template' optional, as new resumes will be uploaded files, not built from templates.
    # Existing resumes linked to templates will keep their template ID.
    template = models.ForeignKey(ResumeCvTemplate, on_delete=models.SET_NULL, related_name="resume_cvs", null=True, blank=True)
    
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    
    # Keep content and style nullable for backward compatibility with old builder resumes
    # or if you ever decide to process HTML/CSS directly from uploaded files.
    content = models.TextField(null=True, blank=True)
    style = models.TextField(null=True, blank=True)
    
    # NEW FIELD: For storing the actual uploaded resume file (e.g., PDF, DOCX)
    resume_file = models.FileField(upload_to=resume_cv_directory_path, blank=True, null=True) 

    is_published = models.BooleanField(default=True)
    view_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True) # This can serve as 'uploaded_at'
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Resume/CV"
        verbose_name_plural = "Resumes/CVs"
