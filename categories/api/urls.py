# D:\django-job-portal-master\categories\api\urls.py

from django.urls import path
from rest_framework import generics
from categories.models import Category
from jobsapp.api.serializers import CategorySerializer # Assuming CategorySerializer is defined here

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [] 

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='api-category-list'),
]

