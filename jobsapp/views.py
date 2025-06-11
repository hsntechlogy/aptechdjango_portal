    # D:\django-job-portal-master\jobsapp\views.py (COMPLETE FILE)

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, JsonResponse, HttpResponseNotAllowed
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView, TemplateView, View, UpdateView # <<< UpdateView added here
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model # For CustomUser and Notification logic

    # Import models from their respective apps
from .models import Job, Applicant, Favorite # Models within jobsapp
from jobs.models import Company, CompanyReview # Models from the 'jobs' app
from notifications.models import Notification # Model from the 'notifications' app

    # Import forms
from .forms import CreateJobForm, ApplyJobForm # Forms for jobsapp
    # from accounts.forms import UserLoginForm # Assuming UserLoginForm is from accounts.forms (for LoginView, if you had it here)

    # Import manager for Job model
from .manager import JobManager # For Job.objects = JobManager()

    # Decorators (ensure these are correctly defined in jobsapp/decorators.py if used)
from .decorators import user_is_employer, user_is_employee # Assuming these exist


User = get_user_model() # Define CustomUser


    # --- General Public-Facing Views ---

class HomeView(ListView):
        model = Job
        template_name = "home.html"
        context_object_name = "jobs"

        def get_queryset(self):
            return self.model.objects.unfilled()[:6]

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["trendings"] = self.model.objects.unfilled(created_at__month=timezone.now().month)[:3]
            return context


class AboutUsView(TemplateView):
        template_name = "about_us.html"


class SearchView(ListView):
        model = Job
        template_name = "jobs/search.html"
        context_object_name = "jobs"

        def get_queryset(self):
            return self.model.objects.filter(
                location__contains=self.request.GET.get("location", ""),
                title__contains=self.request.GET.get("position", ""),
            )


class JobListView(ListView):
        model = Job
        template_name = "jobs/jobs.html"
        context_object_name = "jobs"
        paginate_by = 5

        def get_queryset(self):
            return self.model.objects.unfilled()

        def get_context_data(self, **kwargs):
            data = super().get_context_data(**kwargs)
            data["total_jobs"] = self.model.objects.unfilled().count()
            return data


class JobDetailsView(DetailView):
        model = Job
        template_name = "jobs/details.html"
        context_object_name = "job"
        pk_url_kwarg = "id"

        def get_object(self, queryset=None):
            obj = super().get_object(queryset=queryset)
            if obj is None:
                raise Http404("Job doesn't exist.")
            return obj

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            job = self.get_object() 

            if job.company:
                context['reviews'] = job.company.reviews.all().order_by('-created_at')
            else:
                context['reviews'] = [] 
            return context


    # --- Employee Specific Views ---

@method_decorator(login_required(login_url=reverse_lazy("accounts:login")), name='dispatch')
@method_decorator(user_is_employee, name='dispatch')
class EmployeeMyJobsListView(ListView):
        model = Applicant
        template_name = 'jobs/employee/my-applications.html'
        context_object_name = 'applicants'

        def get_queryset(self):
            return self.model.objects.filter(user=self.request.user).order_by('-created_at')

@method_decorator(login_required(login_url=reverse_lazy("accounts:login")), name='dispatch')
@method_decorator(user_is_employee, name='dispatch')
class FavoriteListView(ListView):
        model = Favorite
        template_name = 'jobs/employee/favorites.html'
        context_object_name = 'favorites'

        def get_queryset(self):
            return self.model.objects.filter(user=self.request.user, soft_deleted=False).order_by('-created_at')

class ApplyJobView(CreateView):
        model = Applicant
        form_class = ApplyJobForm
        slug_field = "job_id" 
        slug_url_kwarg = "job_id"

        @method_decorator(login_required(login_url=reverse_lazy("accounts:login")))
        @method_decorator(user_is_employee)
        def dispatch(self, request, *args, **kwargs):
            return super().dispatch(self.request, *args, **kwargs)

        def get(self, request, *args, **kwargs):
            return HttpResponseNotAllowed(self._allowed_methods())

        def post(self, request, *args, **kwargs):
            form = self.get_form()
            if form.is_valid():
                messages.info(self.request, "Successfully applied for the job!")
                return self.form_valid(form)
            else:
                messages.error(self.request, "Error applying for the job. Please check your form.")
                return HttpResponseRedirect(reverse_lazy("jobs:jobs-detail", kwargs={"id": self.kwargs["job_id"]}))

        def get_success_url(self):
            return reverse_lazy("jobs:jobs-detail", kwargs={"id": self.kwargs["job_id"]})

        def form_valid(self, form):
            applicant = Applicant.objects.filter(user=self.request.user, job_id=self.kwargs["job_id"])
            if applicant.exists():
                messages.info(self.request, "You already applied for this job")
                return HttpResponseRedirect(self.get_success_url())
            
            form.instance.user = self.request.user
            form.instance.job = Job.objects.get(id=self.kwargs["job_id"])
            form.save()
            return super().form_valid(form)


    # --- Employer Specific Views ---

@method_decorator(login_required(login_url=reverse_lazy("accounts:login")), name='dispatch')
@method_decorator(user_is_employer, name='dispatch')
class DashboardView(TemplateView):
        template_name = 'jobs/employer/dashboard.html'

@method_decorator(login_required(login_url=reverse_lazy("accounts:login")), name='dispatch')
@method_decorator(user_is_employer, name='dispatch')
class ApplicantsListView(ListView):
        model = Applicant
        template_name = 'jobs/employer/all-applicants.html'
        context_object_name = 'applicants'

        def get_queryset(self):
            return self.model.objects.filter(job__user=self.request.user).order_by('-created_at')

@method_decorator(login_required(login_url=reverse_lazy("accounts:login")), name='dispatch')
@method_decorator(user_is_employer, name='dispatch')
class ApplicantPerJobView(ListView):
        model = Applicant
        template_name = 'jobs/employer/applicants.html'
        context_object_name = 'applicants'

        def get_queryset(self):
            job_id = self.kwargs.get('job_id')
            return self.model.objects.filter(job_id=job_id, job__user=self.request.user).order_by('-created_at')

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            job_id = self.kwargs.get('job_id')
            context['job'] = get_object_or_404(Job, id=job_id, user=self.request.user)
            return context

@method_decorator(login_required(login_url=reverse_lazy("accounts:login")), name='dispatch')
@method_decorator(user_is_employer, name='dispatch')
class AppliedApplicantView(DetailView):
        model = Applicant
        template_name = 'jobs/employer/applied-applicant-view.html'
        context_object_name = 'applicant'
        pk_url_kwarg = "applicant_id"

        def get_object(self, queryset=None):
            applicant = super().get_object(queryset=queryset)
            if not applicant.job.user == self.request.user:
                raise Http404("You are not authorized to view this applicant.")
            return applicant


@method_decorator(login_required(login_url=reverse_lazy("accounts:login")), name='dispatch')
@method_decorator(user_is_employer, name='dispatch')
class JobCreateView(CreateView):
        model = Job
        form_class = CreateJobForm
        template_name = 'jobsapp/job_form.html'
        success_url = reverse_lazy('jobs:jobs')

        def form_valid(self, form):
            job = form.save(commit=False)
            job.user = self.request.user
            job.save()
            form.save_m2m() # Save ManyToMany relations (like tags) if any

            # --- NOTIFICATION LOGIC ---
            users_to_notify = User.objects.filter(is_active=True)
            users_to_notify = users_to_notify.exclude(pk=self.request.user.pk)
            users_to_notify = users_to_notify.exclude(is_staff=True).exclude(is_superuser=True)
            # users_to_notify = users_to_notify.exclude(is_company=True) # Uncomment if you want to exclude other employers/companies
            
            # --- DEBUGGING: Print the users being notified ---
            print(f"DEBUG: Total active users: {User.objects.filter(is_active=True).count()}")
            print(f"DEBUG: Job poster (excluded): {self.request.user.email} (ID: {self.request.user.pk})")
            print(f"DEBUG: Staff users (excluded): {User.objects.filter(is_staff=True).count()}")
            print(f"DEBUG: Superusers (excluded): {User.objects.filter(is_superuser=True).count()}")
            
            # Filter to only notify employee roles specifically
            users_to_notify = users_to_notify.filter(role='employee')
            print(f"DEBUG: Users eligible for notification (role='employee'): {users_to_notify.count()}")

            for user_account in users_to_notify:
                print(f"  - Eligible user: {user_account.email} (ID: {user_account.id})")
                Notification.objects.create(
                    user=user_account,
                    message=f"New Job Posted: {job.title}" 
                )
            # --- END NOTIFICATION LOGIC ---
            
            messages.success(self.request, f"Job '{job.title}' posted successfully!")
            return super().form_valid(form)


@method_decorator(login_required(login_url=reverse_lazy("accounts:login")), name='dispatch')
@method_decorator(user_is_employer, name='dispatch')
class JobUpdateView(UpdateView):
        model = Job
        form_class = CreateJobForm
        template_name = 'jobsapp/job_form.html'
        pk_url_kwarg = 'id'
        success_url = reverse_lazy('jobs:employer-dashboard')

        def get_queryset(self):
            return self.model.objects.filter(user=self.request.user)

        def form_valid(self, form):
            messages.success(self.request, "Job updated successfully!")
            return super().form_valid(form)


    # --- Utility Functions / Views ---

def filled(request, job_id):
        if not request.user.is_authenticated or not request.user.is_employer:
            return JsonResponse({'status': 'error', 'message': 'Authentication required or not an employer.'}, status=403)
        
        job = get_object_or_404(Job, id=job_id, user=request.user)
        job.filled = True
        job.save()
        messages.success(request, f"Job '{job.title}' marked as filled!")
        return redirect('jobs:employer-dashboard-applicants', job_id=job.id)


class SendResponseView(View):
        @method_decorator(login_required(login_url=reverse_lazy("accounts:login")), name='dispatch')
        @method_decorator(user_is_employer, name='dispatch')
        def dispatch(self, request, *args, **kwargs):
            return super().dispatch(self.request, *args, **kwargs)

        def post(self, request, applicant_id):
            applicant = get_object_or_404(Applicant, id=applicant_id, job__user=request.user)
            message_text = request.POST.get('message_text', '').strip()

            if not message_text:
                messages.error(request, "Message cannot be empty.")
                return redirect('jobs:applied-applicant-view', job_id=applicant.job.id, applicant_id=applicant.id)

            Notification.objects.create(
                user=applicant.user,
                message=f"Response from {request.user.email} for your application to '{applicant.job.title}': {message_text}"
            )
            messages.success(request, "Response sent to applicant.")
            return redirect('jobs:applied-applicant-view', job_id=applicant.job.id, applicant_id=applicant.id)


def favorite(request):
        if not request.user.is_authenticated:
            return JsonResponse(data={"auth": False, "status": "error", "message": "Authentication required"}, status=401)

        job_id = request.POST.get("job_id")
        if not job_id:
            return JsonResponse(data={"auth": True, "status": "error", "message": "Job ID not provided"}, status=400)

        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return JsonResponse(data={"auth": True, "status": "error", "message": "Job not found"}, status=404)

        fav, created = Favorite.objects.get_or_create(user=request.user, job=job)
        
        if not created and not fav.soft_deleted:
            fav.soft_deleted = True
            fav.save()
            return JsonResponse(
                data={"auth": True, "status": "removed", "message": "Job removed from your favorite list"}
            )
        elif not created and fav.soft_deleted:
            fav.soft_deleted = False
            fav.save()
            return JsonResponse(data={"auth": True, "status": "added", "message": "Job added to your favorite list"})
        else:
            return JsonResponse(data={"auth": True, "status": "added", "message": "Job added to your favorite list"})

    # --- Company & Review Views ---

class CompanyDetailView(DetailView):
        model = Company 
        template_name = 'jobs/company_details.html'
        context_object_name = 'company'
        pk_url_kwarg = 'pk'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            company = self.get_object()
            context['jobs_by_company'] = company.jobs.filter(is_published=True).order_by('-created_at')
            context['reviews'] = company.reviews.all().order_by('-created_at')
            return context


def add_review(request, company_id):
        company = get_object_or_404(Company, id=company_id)

        if request.method == 'POST':
            if not request.user.is_authenticated:
                messages.error(request, "You must be logged in to leave a review.")
                return redirect('accounts:login')

            try:
                rating = int(request.POST.get('rating'))
                if not (1 <= rating <= 5):
                    raise ValueError("Rating must be between 1 and 5.")
            except (ValueError, TypeError):
                messages.error(request, "Invalid rating. Please enter a number between 1 and 5.")
                return render(request, 'jobs/add_review.html', {'company': company})

            comment = request.POST.get('comment', '').strip()
            if not comment:
                messages.error(request, "Comment cannot be empty.")
                return render(request, 'jobs/add_review.html', {'company': company})

            CompanyReview.objects.create(company=company, user=request.user, rating=rating, comment=comment)
            messages.success(request, "Your review has been submitted!")
            return redirect('jobs:company_detail', pk=company.id)

        return render(request, 'jobs/add_review.html', {'company': company})
    