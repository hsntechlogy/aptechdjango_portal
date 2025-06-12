# D:\django-job-portal-master\jobsapp\api\serializers.py

from rest_framework import serializers
from jobsapp.models import Job, Applicant, Favorite # Assuming these models are in jobsapp.models
from accounts.models import CustomUser # Assuming CustomUser is your AUTH_USER_MODEL
from jobs.models import Company, CompanyReview # Assuming Company and CompanyReview are in jobs.models
from categories.models import Category # Assuming Category is in categories.models
from tags.models import Tag # Assuming Tag is in tags.models


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'description', 'website') # Include fields you want to expose


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class JobSerializer(serializers.ModelSerializer):
    # Nested serializers for related objects to provide more detail
    company = CompanySerializer(read_only=True) # Read-only, automatically populated
    category = CategorySerializer(read_only=True) # Read-only, automatically populated
    tags = TagSerializer(many=True, read_only=True) # Many-to-many, read-only

    # If you want to allow creating/updating jobs via API with company ID and category ID
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), source='company', write_only=True, required=False
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    tag_ids = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all()),
        write_only=True, required=False, allow_empty=True
    )

    class Meta:
        model = Job
        fields = (
            'id', 'title', 'location', 'salary', 'description', 
            'type', 'vacancy', 'last_date', 'is_published', 'filled', 
            'created_at', 'apply_url',
            'company', 'category', 'tags', # Nested objects for read
            'company_id', 'category_id', 'tag_ids' # IDs for write
        )
        read_only_fields = ('user', 'created_at') # User is set by the view


    def create(self, validated_data):
        tag_ids = validated_data.pop('tag_ids', [])
        job = Job.objects.create(**validated_data)
        if tag_ids:
            job.tags.set(tag_ids)
        return job

    def update(self, instance, validated_data):
        tag_ids = validated_data.pop('tag_ids', [])
        
        # Update fields that are not nested or M2M
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tag_ids:
            instance.tags.set(tag_ids)
        else:
            instance.tags.clear() # Clear tags if none provided
        
        return instance


class ApplicantSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)
    cv_url = serializers.FileField(source='cv', read_only=True) # Expose CV URL

    class Meta:
        model = Applicant
        fields = ('id', 'user', 'job', 'status', 'applied_at', 'cv', 'user_email', 'job_title', 'cv_url')
        read_only_fields = ('user', 'job', 'applied_at') # User and job are set by the view


class FavoriteSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    job_location = serializers.CharField(source='job.location', read_only=True)

    class Meta:
        model = Favorite
        fields = ('id', 'user', 'job', 'soft_deleted', 'created_at', 'job_title', 'job_location')
        read_only_fields = ('user', 'job', 'created_at')
