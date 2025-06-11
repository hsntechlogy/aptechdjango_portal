# D:\django-job-portal-master\jobs\views.py

from notifications.models import Notification
from django import forms # Assuming this is django.forms, not an instance
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from .models import Company, CompanyReview # Assuming these models are in jobs/models.py

# IMPORTANT: The following block of code is problematic because it runs at the module level
# during Django startup, attempting to access the database before tables are created.
# It also has a logical error with `forms.save()`.
# It should be moved inside a function (e.g., a view that creates a job) or a Django signal.
"""
MyUser = get_user_model()
for user in MyUser.objects.exclude(is_staff=True):
    # This `forms.save()` is likely incorrect. It seems to refer to the `django.forms` module.
    # You'd typically save a specific form instance, like `job_form.save()`.
    job = forms.save()
    Notification.objects.create(user=user, message=f"New Job Posted: {job.title}")
"""

def add_review(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    if request.method == 'POST':
        rating = request.POST['rating']
        comment = request.POST['comment']
        CompanyReview.objects.create(company=company, user=request.user, rating=rating, comment=comment)
        return redirect('company_detail', company_id=company.id)
    return render(request, 'jobs/add_review.html', {'company': company})

# ... other views or code ...