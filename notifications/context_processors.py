# D:\django-job-portal-master\notifications\context_processors.py
from notifications.models import Notification

def notifications_count(request):
    """
    Context processor to add the count of unread notifications for the logged-in user.
    """
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        return {'notifications_count': unread_count} # THIS IS THE CORRECT KEY
    return {'notifications_count': 0} # Return 0 if user is not authenticated