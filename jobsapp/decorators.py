# D:\django-job-portal-master\jobsapp\decorators.py

from django.http import JsonResponse, HttpResponseForbidden
from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages

def user_is_employee(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'employee':
            return function(request, *args, **kwargs)
        else:
            # Check if the request is an AJAX request
            # This header is commonly sent by JavaScript's Fetch API and jQuery's AJAX
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                # For AJAX requests, return a JSON error response with 403 Forbidden status
                return JsonResponse({'error': 'Permission Denied: Employee role required.'}, status=403)
            else:
                # For regular browser requests (non-AJAX), redirect with a message
                messages.error(request, "You must be logged in as an employee to access this page.")
                return redirect(reverse_lazy('accounts:login'))
    return wrap

def user_is_employer(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'employer':
            return function(request, *args, **kwargs)
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Permission Denied: Employer role required.'}, status=403)
            else:
                messages.error(request, "You must be logged in as an employer to access this page.")
                return redirect(reverse_lazy('accounts:login'))
    return wrap
