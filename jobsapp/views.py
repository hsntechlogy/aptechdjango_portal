# D:\django-job-portal-master\jobsapp\views.py (MONOLITHIC FILE)

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404, HttpResponseRedirect, JsonResponse, HttpResponseNotAllowed, HttpResponse 
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator 
from django.utils.translation import gettext_lazy as _ 
from django.views.generic import CreateView, DetailView, ListView, TemplateView, View, UpdateView

# Import models from their respective apps
from jobsapp.models import Job, Applicant, Favorite 
from jobs.models import Company, CompanyReview # Assuming Company and CompanyReview are in jobs/models.py
from notifications.models import Notification # Import the Notification model

# Import forms
from jobsapp.forms import CreateJobForm, ApplyJobForm

# Import decorators (ensure these are correctly defined in jobsapp/decorators.py)
from jobsapp.decorators import user_is_employer, user_is_employee 


User = get_user_model()


# --- Mixins for Role-Based Access Control ---
class EmployeeRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'employee'
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, _("Access denied. Only employees can view this page."))
        else:
            messages.error(self.request, _("You must be logged in to view this page."))
        return super().handle_no_permission()


class EmployerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'employer'

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, _("Access denied. Only employers can view this page."))
        else:
            messages.error(self.request, _("You must be logged in to view this page."))
        return super().handle_no_permission()

class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin): 
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff 

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, _("Access denied. Only admin users can view this page."))
        else:
            messages.error(self.request, _("You must be logged in to view this page."))
        return super().handle_no_permission()


# --- General Public-Facing Views ---

class HomeView(ListView):
    model = Job
    template_name = "home.html" 
    context_object_name = "jobs"

    def get_queryset(self):
        return self.model.objects.filter(filled=False, is_published=True).order_by('-created_at')[:6]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_jobs"] = self.model.objects.filter(is_published=True, filled=False).count()
        context["trendings"] = self.model.objects.filter(
            filled=False, is_published=True, created_at__month=timezone.now().month
        ).order_by('-created_at')[:3]
        return context


class AboutUsView(TemplateView):
    template_name = "about_us.html" 


class SearchView(ListView):
    model = Job
    template_name = "jobs/search.html" 
    context_object_name = "jobs"
    paginate_by = 10 

    def get_queryset(self):
        location_query = self.request.GET.get("location", "").strip()
        position_query = self.request.GET.get("position", "").strip()
        category_query = self.request.GET.get("category", "").strip() 
        tag_query = self.request.GET.get("tag", "").strip() 

        queryset = self.model.objects.filter(filled=False, is_published=True)

        if location_query:
            queryset = queryset.filter(location__icontains=location_query)
        if position_query:
            queryset = queryset.filter(title__icontains=position_query)
        if category_query:
            queryset = queryset.filter(category__slug=category_query) 
        if tag_query:
            queryset = queryset.filter(tags__slug=tag_query) 
        
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from categories.models import Category
        from tags.models import Tag
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        context['selected_location'] = self.request.GET.get('location', '')
        context['selected_position'] = self.request.GET.get('position', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_tag'] = self.request.GET.get('tag', '')
        return context


class JobListView(ListView):
    model = Job
    template_name = "jobs/jobs.html" 
    context_object_name = "jobs"
    paginate_by = 10 

    def get_queryset(self):
        return self.model.objects.filter(filled=False, is_published=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["total_jobs"] = self.model.objects.filter(filled=False, is_published=True).count()
        return data


class JobDetailsView(DetailView):
    model = Job
    template_name = "jobs/job_detail.html" 
    context_object_name = "job"
    pk_url_kwarg = "id"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj is None:
            raise Http404(_("Job doesn't exist."))
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.get_object() 

        context['apply_form'] = ApplyJobForm()

        if self.request.user.is_authenticated and self.request.user.role == 'employee':
            context['has_applied'] = Applicant.objects.filter(user=self.request.user, job=job).exists()
        else:
            context['has_applied'] = False

        # Assuming company has a related_name 'reviews' for CompanyReview
        if job.company:
            context['reviews'] = job.company.reviews.all().order_by('-created_at')
        else:
            context['reviews'] = [] 
        return context


# --- Employee Specific Views ---

class EmployeeMyApplicationsView(EmployeeRequiredMixin, ListView): 
    model = Applicant
    template_name = 'jobs/employee/my_applications.html'
    context_object_name = 'applications' 
    paginate_by = 10 

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).order_by('-applied_at')


class FavoriteListView(EmployeeRequiredMixin, ListView):
    model = Favorite 
    template_name = 'jobs/employee/favorites.html'
    context_object_name = 'favorites'
    paginate_by = 10 

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user, soft_deleted=False).order_by('-created_at')


class ApplyJobView(EmployeeRequiredMixin, CreateView): 
    model = Applicant
    form_class = ApplyJobForm
    template_name = 'jobs/employee/apply_job_form.html' 
    success_url = reverse_lazy('jobsapp:employee-my-applications') 
    
    def dispatch(self, request, *args, **kwargs):
        self.job = get_object_or_404(Job, id=self.kwargs['job_id'])
        if Applicant.objects.filter(user=self.request.user, job=self.job).exists():
            messages.info(self.request, _("You have already applied for this job."))
            return redirect('jobsapp:jobs-detail', id=self.job.id) 
        
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = self.job 
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.job = self.job
        
        messages.success(self.request, _(f"Successfully applied for '{self.job.title}'!"))

        # --- CRITICAL ADDITION FOR EMPLOYER NOTIFICATION ON NEW APPLICATION ---
        # Notify the employer who owns this job
        if self.job.user: # Ensure the job has an associated employer
            Notification.objects.create(
                user=self.job.user, # The employer (job poster)
                message=_(f"New application for your job '{self.job.title}' from {self.request.user.get_full_name() or self.request.user.email}.")
            )
        # --- END CRITICAL ADDITION ---

        return super().form_valid(form) 


# --- Employer Specific Views ---

# D:\django-job-portal-master\jobsapp\views.py
class DashboardView(EmployerRequiredMixin, ListView): 
    model = Job
    template_name = 'jobs/employer/dashboard.html'
    context_object_name = 'jobs'
    ordering = ['-created_at']

    def get_queryset(self):
        # This line correctly filters jobs by the currently logged-in user (employer)
        return Job.objects.filter(user=self.request.user).order_by('-created_at')


class ApplicantsListView(EmployerRequiredMixin, ListView): 
    model = Applicant
    template_name = 'jobs/employer/all_applicants.html' 
    context_object_name = 'applicants'
    paginate_by = 10 

    def get_queryset(self):
        queryset = self.model.objects.filter(job__user=self.request.user)

        status_filter = self.request.GET.get('status')
        if status_filter:
            try:
                queryset = queryset.filter(status=int(status_filter))
            except ValueError:
                pass 

        return queryset.order_by('-applied_at')


class ApplicantPerJobView(EmployerRequiredMixin, ListView):
    model = Applicant
    template_name = 'jobs/employer/applicants.html' 
    context_object_name = 'applicants'
    paginate_by = 10 

    def get_queryset(self):
        job_id = self.kwargs.get('job_id')
        return self.model.objects.filter(job_id=job_id, job__user=self.request.user).order_by('-applied_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_id = self.kwargs.get('job_id')
        context['job'] = get_object_or_404(Job, id=job_id, user=self.request.user)
        return context


class AppliedApplicantView(EmployerRequiredMixin, DetailView):
    model = Applicant
    template_name = 'jobs/employer/applied_applicant_view.html' 
    context_object_name = 'applicant'
    pk_url_kwarg = "applicant_id"

    def get_object(self, queryset=None):
        applicant = super().get_object(queryset=queryset)
        if not applicant.job.user == self.request.user:
            raise Http404(_("You are not authorized to view this applicant."))
        return applicant


class JobCreateView(EmployerRequiredMixin, CreateView):
    model = Job
    form_class = CreateJobForm 
    template_name = 'jobs/employer/job_form.html' 
    success_url = reverse_lazy('jobsapp:employer-dashboard') 

    def form_valid(self, form):
        company_name = form.cleaned_data.pop('company_name')
        company_description = form.cleaned_data.pop('company_description')
        website = form.cleaned_data.pop('website')
        
        try:
            company, created = Company.objects.get_or_create(user=self.request.user)
            company.name = company_name
            company.description = company_description
            company.website = website
            company.save()
        except Exception as e:
            messages.error(self.request, _(f"Error saving company details: {e}"))
            form.cleaned_data['company_name'] = company_name 
            form.cleaned_data['company_description'] = company_description
            form.cleaned_data['website'] = website
            return self.form_invalid(form) 

        job = form.save(commit=False)
        job.user = self.request.user
        job.company = company 
        job.is_published = True 
        job.save() 
        
        form.save_m2m() 

        # Notify all active employee users about the new job posting
        users_to_notify = User.objects.filter(is_active=True, role='employee') \
                                     .exclude(pk=self.request.user.pk) \
                                     .exclude(is_staff=True) \
                                     .exclude(is_superuser=True)
        
        for user_account in users_to_notify:
            try:
                Notification.objects.create(
                    user=user_account,
                    message=_(f"New Job Posted: {job.title} by {job.company.name if job.company else 'Unknown Company'}") 
                )
            except Exception as e:
                print(f"ERROR: Failed to create notification for {user_account.email}: {e}")
        
        messages.success(self.request, _(f"Job '{job.title}' posted successfully!"))
        return super().form_valid(form) 


class JobUpdateView(EmployerRequiredMixin, UpdateView):
    model = Job
    form_class = CreateJobForm 
    template_name = 'jobs/employer/job_form.html' 
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('jobsapp:employer-dashboard') 

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def form_valid(self, form):
        company_name = form.cleaned_data.pop('company_name')
        company_description = form.cleaned_data.pop('company_description')
        website = form.cleaned_data.pop('website')
        
        try:
            company, created = Company.objects.get_or_create(user=self.request.user)
            company.name = company_name
            company.description = company_description
            company.website = website
            company.save()
        except Exception as e:
            messages.error(self.request, _(f"Error updating company details: {e}"))
            form.cleaned_data['company_name'] = company_name 
            form.cleaned_data['company_description'] = company_description
            form.cleaned_data['website'] = website
            return self.form_invalid(form)

        job = form.save(commit=False)
        job.company = company 
        job.is_published = True 
        job.save()
        form.save_m2m() 

        messages.success(self.request, "Job updated successfully!")
        return super().form_valid(form) 


# --- Utility Functions / Views (Shared) ---

@login_required
@user_is_employer
def job_filled_view(request, job_id): 
    if request.method == 'POST': 
        job = get_object_or_404(Job, id=job_id, user=request.user)
        job.filled = True
        job.save()
        messages.success(request, _(f"Job '{job.title}' marked as filled!"))
        return redirect('jobsapp:employer-dashboard-applicants', job_id=job.id) 
    else:
        return HttpResponseNotAllowed(['POST'])


class SendResponseView(View):
    @method_decorator(login_required(login_url=reverse_lazy("accounts:login")), name='dispatch')
    @method_decorator(user_is_employer, name='dispatch')
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, applicant_id):
        applicant = get_object_or_404(Applicant, id=applicant_id, job__user=request.user)
        message_text = request.POST.get('message_text', '').strip()
        new_status = request.POST.get('status') 

        if not message_text:
            messages.error(request, _("Message cannot be empty."))
            return redirect('jobsapp:applied-applicant-view', job_id=applicant.job.id, applicant_id=applicant.id)

        try:
            if new_status:
                # Ensure status is an integer before setting
                applicant.status = int(new_status) 
                applicant.save()
                messages.info(request, _(f"Applicant status updated to {applicant.get_status_display()}."))

            # --- CRITICAL ADDITION FOR EMPLOYEE NOTIFICATION ON STATUS UPDATE ---
            employee_user = applicant.user # The employee who applied
            notification_message = _(
                f"Your application for '{applicant.job.title}' has been updated to '{applicant.get_status_display()}'. "
                f"Employer's message: '{message_text}'"
            )
            
            Notification.objects.create(
                user=employee_user, # Notify the employee
                message=notification_message
            )
            messages.success(request, _("Response sent to applicant."))
            # --- END CRITICAL ADDITION ---

        except Exception as e:
            messages.error(request, _(f"Error sending response: {e}")) 
            print(f"ERROR: Failed to create notification or update status: {e}") 
        
        return redirect('jobsapp:applied-applicant-view', job_id=applicant.job.id, applicant_id=applicant.id)


def favorite(request):
    if not request.user.is_authenticated:
        return JsonResponse(data={"auth": False, "status": "error", "message": _("Authentication required")}, status=401)

    job_id = request.POST.get("job_id")
    if not job_id:
        return JsonResponse(data={"auth": True, "status": "error", "message": _("Job ID not provided")}, status=400)

    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return JsonResponse(data={"auth": True, "status": "error", "message": _("Job not found")}, status=404)

    fav, created = Favorite.objects.get_or_create(user=request.user, job=job)
    
    if not created and not fav.soft_deleted: 
        fav.soft_deleted = True
        fav.save()
        return JsonResponse(
            data={"auth": True, "status": "removed", "message": _("Job removed from your favorite list")}
        )
    elif not created and fav.soft_deleted: 
        fav.soft_deleted = False
        fav.save()
        return JsonResponse(data={"auth": True, "status": "added", "message": _("Job added to your favorite list")})
    else: 
        return JsonResponse(data={"auth": True, "status": "added", "message": _("Job added to your favorite list")})


# --- Company & Review Views ---

class CompanyListView(ListView):
    model = Company
    template_name = 'jobs/company_list.html'
    context_object_name = 'companies'

class CompanyDetailView(DetailView):
    model = Company 
    template_name = 'jobs/company_details.html' # Note: previously company/detail.html and jobs/company_detail.html were shown, ensuring consistent path
    context_object_name = 'company'
    pk_url_kwarg = 'pk' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = self.get_object()
        context['jobs_by_company'] = company.jobs.filter(is_published=True, filled=False).order_by('-created_at')
        # Assuming Company model has a related_name 'reviews' for CompanyReview
        context['reviews'] = company.reviews.all().order_by('-created_at') 
        return context


@login_required
def add_review(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    if request.method == 'POST':
        # Removed explicit request.user.is_authenticated check as @login_required handles it
        
        # Ensure only employees can add reviews
        if request.user.role != 'employee':
            messages.error(request, _("Access denied. Only employees can add reviews."))
            return redirect('jobsapp:company_detail', pk=company.id)

        try:
            rating = int(request.POST.get('rating'))
            if not (1 <= rating <= 5):
                raise ValueError(_("Rating must be between 1 and 5."))
        except (ValueError, TypeError):
            messages.error(request, _("Invalid rating. Please enter a number between 1 and 5."))
            return redirect('jobsapp:company_detail', pk=company.id) 

        comment = request.POST.get('comment', '').strip()
        if not comment:
            messages.error(request, _("Comment cannot be empty."))
            return redirect('jobsapp:company_detail', pk=company.id)

        existing_review = CompanyReview.objects.filter(company=company, user=request.user).first()
        if existing_review:
            messages.warning(request, _("You have already submitted a review for this company. You can edit your existing review."))
            return redirect('jobsapp:company_detail', pk=company.id)

        try:
            CompanyReview.objects.create(company=company, user=request.user, rating=rating, comment=comment)
            messages.success(request, _("Your review has been submitted!"))

            # --- CRITICAL ADDITION 1: Notify the employee about THEIR review submission ---
            Notification.objects.create(
                user=request.user, # The employee who submitted the review
                message=_(f"Your review for '{company.name}' was successfully submitted with a rating of {rating} stars.")
            )
            # --- END CRITICAL ADDITION 1 ---

            # --- CRITICAL ADDITION 2: Notify the employer (company owner) about the new review ---
            if company.user: # Assuming Company model has a 'user' ForeignKey to the employer
                Notification.objects.create(
                    user=company.user, # The employer who owns the company
                    message=_(f"Your company '{company.name}' received a new {rating}-star review from {request.user.get_full_name() or request.user.email}.")
                )
            # --- END CRITICAL ADDITION 2 ---

        except Exception as e:
            messages.error(request, _(f"Error saving review: {e}")) 
            print(f"ERROR: Failed to create review or notifications: {e}") 
        
        return redirect('jobsapp:company_detail', pk=company.id) 

    return redirect('jobsapp:company_detail', pk=company.id) 


# --- Placeholder Error Handler Views ---
def custom_bad_request_view(request, exception=None): 
    """400 Bad Request error handler."""
    return render(request, 'errors/400.html', {'exception': exception}, status=400)

def custom_permission_denied_view(request, exception=None): 
    """403 Forbidden error handler."""
    return render(request, 'errors/403.html', {'exception': exception}, status=403)

def custom_page_not_found_view(request, exception=None): 
    """404 Not Found error handler."""
    return render(request, 'errors/404.html', {'exception': exception}, status=404)

def custom_server_error_view(request):
    """500 Server Error handler."""
    return render(request, 'errors/500.html', {}, status=500)
