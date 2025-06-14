# D:\django-job-portal-master\jobsapp\templatetags\jobsapp_tags.py

from django import template
from jobsapp.models import Applicant, Favorite # Import your models here

register = template.Library()

@register.simple_tag
def is_already_applied(user, job):
    """
    Checks if a given user has already applied for a specific job.
    Returns True if applied, False otherwise.
    Usage in template: {% is_already_applied user job as has_applied %}
    """
    # Check if the user is authenticated before querying
    if not user.is_authenticated:
        return False
    # Check if an Applicant record exists for this user and job
    return Applicant.objects.filter(user=user, job=job).exists()

@register.simple_tag
def is_favorited(user, job):
    """
    Checks if a given user has favorited a specific job (and it's not soft-deleted).
    Returns True if favorited, False otherwise.
    Usage in template: {% is_favorited user job as is_already_favorited %}
    """
    # Check if the user is authenticated before querying
    if not user.is_authenticated:
        return False
    # Check if a Favorite record exists for this user and job, and it's not soft-deleted
    return Favorite.objects.filter(user=user, job=job, soft_deleted=False).exists()

