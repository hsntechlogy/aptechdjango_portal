# D:\django-job-portal-master\tags\api\urls.py

from django.urls import path
from rest_framework import generics
from tags.models import Tag
from jobsapp.api.serializers import TagSerializer # Assuming TagSerializer is defined here

class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializer
    permission_classes = [] 

urlpatterns = [
    path('tags/', TagListAPIView.as_view(), name='api-tag-list'),
]

