# D:\django-job-portal-master\jobsapp\templatetags\is_already_applied.py

from django import template
from jobsapp.models import Applicant # Import the Applicant model

register = template.Library()

@register.simple_tag
def is_already_applied(job, user):
    """
    Checks if the given user has already applied for the given job.
    Usage: {% is_already_applied job request.user as is_applied %}
           {% if is_applied %} ... {% endif %}
    """
    if not user.is_authenticated:
        return False
    # Check if an Applicant record exists for this job and user
    return Applicant.objects.filter(job=job, user=user).exists()

