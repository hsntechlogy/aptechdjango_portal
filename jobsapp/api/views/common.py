    # D:\django-job-portal-master\jobsapp\api\views\common.py

from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from jobsapp.models import Job # Import Job model directly

from jobsapp.api.serializers import JobSerializer


class JobViewSet(viewsets.ReadOnlyModelViewSet):
        serializer_class = JobSerializer
        queryset = Job.objects.unfilled() 
        permission_classes = [AllowAny]


class SearchApiView(ListAPIView):
        serializer_class = JobSerializer
        permission_classes = [AllowAny]

        def get_queryset(self):
            if "location" in self.request.GET and "position" in self.request.GET:
                return Job.objects.unfilled(
                    location__contains=self.request.GET["location"],
                    title__contains=self.request.GET["position"],
                )
            else:
                return Job.objects.unfilled()
    