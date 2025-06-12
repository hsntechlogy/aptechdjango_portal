from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages # Import messages for feedback
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()

@login_required
def employee_notifications(request):
    """
    Displays notifications for the currently logged-in user.
    Only accessible by authenticated users.
    """
    print(f"DEBUG: Accessing employee_notifications for user: {request.user.email} (ID: {request.user.id})")
    # Ensure notifications are fetched for the current user and ordered by creation time
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    print(f"DEBUG: Found {notifications.count()} notifications for {request.user.email}.")
    
    # Render the notifications list template, passing the fetched notifications
    # Ensure 'notifications/list.html' exists and extends base.html
    return render(request, 'notifications/list.html', {'notifications': notifications})

@login_required
def create_notification_for_employees(request):
    """
    Allows an admin to create a notification for all employees.
    This is for demonstration/admin use, usually part of a bigger admin panel.
    """
    print(f"DEBUG: create_notification_for_employees accessed by user: {request.user.email}, role: {request.user.role}")
    # Restrict this view to only 'admin' role users for security
    if request.user.role != 'admin':
        messages.error(request, "You are not authorized to create notifications.")
        return redirect('jobsapp:home') # Redirect to home or employee notifications if not admin

    if request.method == 'POST':
        message_text = request.POST.get('message_text', '').strip()
        print(f"DEBUG: Admin notification message received: '{message_text}'")
        if not message_text:
            messages.error(request, "Notification message cannot be empty.")
            # Re-render the form if the message is empty
            return render(request, 'notifications/create_notification.html', {'employees': User.objects.filter(role='employee')}) 
        
        employees = User.objects.filter(role='employee', is_active=True)
        count = 0
        print(f"DEBUG: Attempting to send admin notification to {employees.count()} active employees.")
        for employee in employees:
            try:
                Notification.objects.create(
                    user=employee,
                    message=message_text # Use the message from the form
                )
                count += 1
                print(f"DEBUG: Admin notification sent to {employee.email}")
            except Exception as e:
                print(f"ERROR: Could not create admin notification for {employee.email}: {e}")

        messages.success(request, f"Notification '{message_text}' sent to {count} employees.")
        return redirect('notifications:employee_notifications') # Redirect after successful creation
    
    # For GET requests, render a form to create a notification
    return render(request, 'notifications/create_notification.html', {'employees': User.objects.filter(role='employee')})
