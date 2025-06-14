# D:\django-job-portal-master\jobsapp\api\serializers.py

from rest_framework import serializers
from jobsapp.models import Job, Applicant, Favorite
from accounts.models import CustomUser
from jobs.models import Company, CompanyReview
from categories.models import Category
from tags.models import Tag


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'description', 'website')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class JobSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

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
            'job_type', 'vacancy', 'last_date', 'is_published', 'filled',
            'created_at', 'apply_url',
            'company', 'category', 'tags',
            'company_id', 'category_id', 'tag_ids'
        )
        read_only_fields = ('user', 'created_at')

    def create(self, validated_data):
        tag_ids = validated_data.pop('tag_ids', [])
        job = Job.objects.create(**validated_data)
        if tag_ids:
            job.tags.set(tag_ids)
        return job

    def update(self, instance, validated_data):
        tag_ids = validated_data.pop('tag_ids', [])
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tag_ids:
            instance.tags.set(tag_ids)
        else:
            instance.tags.clear()
        
        return instance


class ApplicantSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)
    cv_url = serializers.FileField(source='cv', read_only=True)

    class Meta:
        model = Applicant
        fields = ('id', 'user', 'job', 'status', 'applied_at', 'cv', 'user_email', 'job_title', 'cv_url')
        read_only_fields = ('user', 'job', 'applied_at')


class FavoriteSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    job_location = serializers.CharField(source='job.location', read_only=True)

    class Meta:
        model = Favorite
        fields = ('id', 'user', 'job', 'soft_deleted', 'created_at', 'job_title', 'job_location')
        read_only_fields = ('user', 'job', 'created_at')

