# D:\django-job-portal-master\tags\api\urls.py

from django.urls import path
from rest_framework import generics
from tags.models import Tag
from jobsapp.api.serializers import TagSerializer # Assuming TagSerializer is defined in jobsapp.api.serializers

# API view for listing Tags
class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializer
    permission_classes = [] # Allow anyone to view tags

urlpatterns = [
    path('tags/', TagListAPIView.as_view(), name='api-tag-list'),
]

