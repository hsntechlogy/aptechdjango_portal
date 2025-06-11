    # D:\django-job-portal-master\jobsapp\api\serializers.py

from rest_framework import serializers

from accounts.models import CustomUser # Import CustomUser directly
from django.contrib.auth import get_user_model

from accounts.api.serializers import UserSerializer
from tags.api.serializers import TagSerializer
from categories.serializers import CategorySerializer # Corrected import path for CategorySerializer

from ..models import Job, Applicant, Favorite # Models from jobsapp
from jobs.models import Company # Company model from 'jobs' app
from categories.models import Category # Category model from 'categories' app
from tags.models import Tag # Tag model from 'tags' app


User = get_user_model()


class JobSerializer(serializers.ModelSerializer):
        user = UserSerializer(read_only=True)
        job_tags = serializers.SerializerMethodField()
        company_name = serializers.CharField(source='company.name', read_only=True)
        company_description = serializers.CharField(source='company.description', read_only=True)
        website = serializers.URLField(source='company.website', read_only=True)
        category = CategorySerializer(read_only=True)


        class Meta:
            model = Job
            fields = "__all__"

        def get_job_tags(self, obj):
            if obj.tags.exists():
                return TagSerializer(obj.tags.all(), many=True).data
            else:
                return []


class DashboardJobSerializer(serializers.ModelSerializer):
        user = UserSerializer(read_only=True)
        job_tags = serializers.SerializerMethodField()
        total_candidates = serializers.SerializerMethodField()
        company_name = serializers.CharField(source='company.name', read_only=True)
        company_description = serializers.CharField(source='company.description', read_only=True)
        category = CategorySerializer(read_only=True)


        class Meta:
            model = Job
            fields = "__all__"

        def get_job_tags(self, obj):
            if obj.tags.exists():
                return TagSerializer(obj.tags.all(), many=True).data
            else:
                return []

        def get_total_candidates(self, obj):
            return obj.applicants.count()


class NewJobSerializer(serializers.ModelSerializer):
        user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())
        company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
        category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=False) # Make category required
        tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, allow_empty=True)


        class Meta:
            model = Job
            fields = (
                'title', 'location', 'salary', 'description', 'company',
                'category', 'tags', 'type', 'vacancy', 'last_date',
                'is_published', 'filled', 'user'
            )


class ApplyJobSerializer(serializers.ModelSerializer):
        class Meta:
            model = Applicant
            fields = ("job",)

        def validate(self, attrs):
            request_user = self.context.get("request", None).user
            if not request_user.is_authenticated:
                raise serializers.ValidationError("Authentication required to apply for jobs.")

            if Applicant.objects.filter(user=request_user, job=attrs.get("job")).exists():
                raise serializers.ValidationError("You have already applied to this job")
            return attrs


class ApplicantSerializer(serializers.ModelSerializer):
        applied_user = serializers.SerializerMethodField()
        job = serializers.SerializerMethodField()
        status = serializers.SerializerMethodField()

        class Meta:
            model = Applicant
            fields = (
                "id",
                "job_id",
                "applied_user",
                "job",
                "status",
                "created_at",
                "comment",
            )

        def get_status(self, obj):
            return obj.get_status

        def get_job(self, obj):
            return JobSerializer(obj.job).data

        def get_applied_user(self, obj):
            return UserSerializer(obj.user).data


class AppliedJobSerializer(serializers.ModelSerializer):
        user = UserSerializer(read_only=True)
        applicant = serializers.SerializerMethodField("_applicant")

        class Meta:
            model = Job
            fields = "__all__"

        def _applicant(self, obj):
            user = self.context.get("request", None).user
            if user and user.is_authenticated:
                try:
                    return ApplicantSerializer(Applicant.objects.get(user=user, job=obj)).data
                except Applicant.DoesNotExist:
                    return None
            return None
    