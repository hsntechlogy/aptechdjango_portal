# D:\django-job-portal-master\jobsapp\api\views\common.py

from rest_framework import generics, permissions, filters 
from jobsapp.models import Job 
from jobsapp.api.serializers import JobSerializer 
from jobs.models import Company # Ensure Company is imported for the perform_create check

# API view for listing and creating jobs
class JobListCreateAPIView(generics.ListCreateAPIView):
    queryset = Job.objects.all().order_by('-created_at') 
    serializer_class = JobSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'location', 'description', 'company__name'] 
    ordering_fields = ['created_at', 'salary', 'last_date'] 

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()] 
        return [permissions.IsAuthenticatedOrReadOnly()] 

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'employer':
            raise permissions.PermissionDenied("Only employers can post jobs.")
        
        # Access the company profile via the related_name on the CustomUser model
        # This assumes the CustomUser model has a OneToOneField to Company with related_name='company_profile'
        try:
            company = user.company_profile 
        except Company.DoesNotExist:
            # If an employer user does not have an associated company profile, prevent job creation.
            raise permissions.PermissionDenied("Employer must have an associated company profile to post jobs. Please update your employer profile.")
        
        serializer.save(user=user, company=company) 


# API view for retrieving, updating, and deleting a specific job
class JobRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView): 
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    lookup_field = 'id' 

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS: 
            return [permissions.IsAuthenticatedOrReadOnly()]
        return [permissions.IsAuthenticated()] 

    def get_queryset(self):
        if self.request.method not in permissions.SAFE_METHODS:
            return self.queryset.filter(user=self.request.user)
        return self.queryset

