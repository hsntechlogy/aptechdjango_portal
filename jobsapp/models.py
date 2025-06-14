# D:\django-job-portal-master\jobsapp\models.py

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from tags.models import Tag # Assuming Tag model exists
from jobs.models import Company # Assuming Company model exists from jobs/models.py

class Job(models.Model):
    # Foreign key to the user (employer) who posted the job
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jobs')
    
    # Foreign key to the Company model - now a direct link
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs', null=True, blank=True)

    title = models.CharField(max_length=255, verbose_name=_("Job Title"))
    description = models.TextField(verbose_name=_("Job Description"))
    location = models.CharField(max_length=255, verbose_name=_("Location"))

    # Job Category (assuming Category model exists in categories app)
    category = models.ForeignKey('categories.Category', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Category"))

    JOB_TYPE_CHOICES = (
        ('full-time', _('Full Time')),
        ('part-time', _('Part Time')),
        ('freelance', _('Freelance')),
        ('internship', _('Internship')),
    )
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full-time', verbose_name=_("Job Type"))

    vacancy = models.PositiveIntegerField(default=1, verbose_name=_("Number of Vacancies"))
    
    # Combined salary field (assuming your form uses a single 'salary' field)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_("Salary"))

    experience = models.CharField(max_length=100, verbose_name=_("Experience Required"), help_text=_("e.g., 2-5 years, Entry-level"), blank=True, null=True)
    
    # Removed gender field as it's not in the new CreateJobForm
    # GENDER_CHOICES = (('male', _('Male')), ('female', _('Female')), ('any', _('Any')),)
    # gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='any', verbose_name=_("Gender Preference"))

    last_date = models.DateField(verbose_name=_("Application Deadline"), null=True, blank=True)
    apply_url = models.URLField(max_length=200, blank=True, null=True, verbose_name=_("External Apply URL"))

    is_published = models.BooleanField(default=True, verbose_name=_("Is Published")) 
    filled = models.BooleanField(default=False, verbose_name=_("Is Filled"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Last Updated"))

    # Many-to-many relationship with Tag model
    tags = models.ManyToManyField(Tag, blank=True, related_name='jobs', verbose_name=_("Tags"))

    class Meta:
        verbose_name = _("Job")
        verbose_name_plural = _("Jobs")
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('jobsapp:jobs-detail', kwargs={'id': self.id})

class Applicant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applicants')
    cv = models.FileField(upload_to='applicants/cvs/', null=True, blank=True, verbose_name=_("Resume/CV")) 
    
    STATUS_CHOICES = (
        (0, _('Pending')),
        (1, _('Reviewed')),
        (2, _('Interview Scheduled')),
        (3, _('Accepted')),
        (4, _('Rejected')),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=0, verbose_name=_("Status"))
    
    applied_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Applied At"))

    class Meta:
        unique_together = ('user', 'job')
        verbose_name = _("Applicant")
        verbose_name_plural = _("Applicants")
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.user.email} applied for {self.job.title}"

# Renamed from FavoriteJob to Favorite for consistency with views.py
class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_favorites')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_favorites')
    created_at = models.DateTimeField(auto_now_add=True)
    soft_deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'job')
        verbose_name = _("Favorite")
        verbose_name_plural = _("Favorites")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} favorited {self.job.title}"

