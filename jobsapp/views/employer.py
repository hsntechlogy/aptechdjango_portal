# D:\django-job-portal-master\jobsapp\views\employer.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    View,
    UpdateView,
    DeleteView,
    ListView,
    CreateView,
    DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.db import IntegrityError
from django.http import Http404, HttpResponseRedirect

from django.utils.decorators import method_decorator # ADDED: Import method_decorator


from accounts.forms import EmployerProfileUpdateForm # Assuming this is used
from accounts.models import CustomUser
from jobsapp.decorators import user_is_employer
from jobsapp.forms import CreateJobForm, ApplyJobForm
from jobsapp.models import Applicant, Job, JobApplication
from notifications.models import Notification
from jobs.models import Company
from tags.models import Tag # ADDED: Import Tag


# --- Dashboard Views ---
class DashboardView(ListView):
    model = Job
    template_name = "jobs/employer/dashboard.html" # Check this path if it's correct (jobs/ or jobsapp/)
    context_object_name = "jobs"

    @method_decorator(login_required(login_url=reverse_lazy("accounts:login")))
    @method_decorator(user_is_employer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class ApplicantPerJobView(ListView):
    model = Applicant
    template_name = "jobs/employer/applicants.html" # Check this path
    context_object_name = "applicants"
    paginate_by = 6

    @method_decorator(login_required(login_url=reverse_lazy("accounts:login")))
    @method_decorator(user_is_employer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Applicant.objects.filter(job_id=self.kwargs["job_id"]).order_by("id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["job"] = Job.objects.get(id=self.kwargs["job_id"])
        return context


# --- Job Creation View ---
class JobCreateView(CreateView):
    # <<< FIXED: TEMPLATE PATH NOW POINTS TO THE CORRECT LOCATION >>>
    template_name = "jobs/create.html" 
    form_class = CreateJobForm
    extra_context = {"title": "Post New Job"}
    success_url = reverse_lazy("jobsapp:employer-dashboard") # Use jobsapp namespace as per earlier config

    @method_decorator(login_required(login_url=reverse_lazy("accounts:login")))
    @method_decorator(user_is_employer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        return context

    def form_valid(self, form):
        try:
            company = Company.objects.get(user=self.request.user)
        except Company.DoesNotExist:
            messages.error(self.request, "You must create a company profile before posting a job. Please go to your profile to create one.")
            return self.form_invalid(form)

        company.name = form.cleaned_data['company_name']
        company.description = form.cleaned_data['company_description']
        company.website = form.cleaned_data['website']
        company.save()

        form.instance.user = self.request.user
        form.instance.company = company
        response = super().form_valid(form)
        
        messages.success(self.request, "Job created successfully!")
        return response

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            messages.error(request, "Please correct the errors below.")
            return self.form_invalid(form)


# --- Job Update View ---
@method_decorator(login_required(login_url=reverse_lazy("accounts:login")), name="dispatch")
@method_decorator(user_is_employer, name="dispatch")
class JobUpdateView(UpdateView):
    template_name = "jobs/update.html" # Check this path
    form_class = CreateJobForm
    extra_context = {"title": "Edit Job"}
    slug_field = "id"
    slug_url_kwarg = "id"
    success_url = reverse_lazy("jobsapp:employer-dashboard") # Use jobsapp namespace
    context_object_name = "job"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Job.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        return context

    def form_valid(self, form):
        try:
            company = Company.objects.get(user=self.request.user)
        except Company.DoesNotExist:
            messages.error(self.request, "Company profile not found for updating.")
            return self.form_invalid(form)

        company.name = form.cleaned_data['company_name']
        company.description = form.cleaned_data['company_description']
        company.website = form.cleaned_data['website']
        company.save()

        messages.success(self.request, "Job updated successfully")
        return super(JobUpdateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            messages.error(request, "Please correct the errors below.")
            return self.form_invalid(form)


# --- All Applicants List View ---
class ApplicantsListView(ListView):
    model = Applicant
    template_name = "jobs/employer/all-applicants.html" # Check this path
    context_object_name = "applicants"

    @method_decorator(login_required(login_url=reverse_lazy("accounts:login")))
    @method_decorator(user_is_employer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        self.queryset = self.model.objects.filter(job__user=self.request.user).order_by("id")
        if "status" in self.request.GET and len(self.request.GET.get("status")) > 0:
            self.queryset = self.queryset.filter(status=int(self.request.GET.get("status")))
        return self.queryset


# --- Function for Setting Job as Filled ---
@login_required(login_url=reverse_lazy("accounts:login"))
@user_is_employer
def filled(request, job_id=None):
    try:
        job = Job.objects.get(user=request.user, id=job_id)
        job.filled = True
        job.save()
        messages.success(request, "Job marked as filled successfully.")
    except Job.DoesNotExist:
        messages.error(request, "Job not found or you don't have permission to modify it.")
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
    
    return HttpResponseRedirect(reverse_lazy("jobsapp:employer-dashboard"))


# --- Applied Applicant Detail View ---
@method_decorator(login_required(login_url=reverse_lazy("accounts:login")), name="dispatch")
@method_decorator(user_is_employer, name="dispatch")
class AppliedApplicantView(DetailView):
    model = Applicant
    template_name = "jobs/employer/applied-applicant-view.html"
    context_object_name = "applicant"
    slug_field = "id"
    slug_url_kwarg = "applicant_id"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Applicant.objects.filter(job__user=self.request.user)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        
        job_id = self.kwargs.get("job_id")
        applicant_id = self.kwargs.get("applicant_id")

        if not job_id or not applicant_id:
            raise Http404("Job ID and Applicant ID are required.")

        try:
            obj = queryset.get(job_id=job_id, id=applicant_id)
        except queryset.model.DoesNotExist:
            raise Http404(
                "No %(verbose_name)s found matching the query for this job." % {"verbose_name": queryset.model._meta.verbose_name}
            )
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# --- Send Response to Applicant View ---
@method_decorator(login_required(login_url=reverse_lazy("accounts:login")), name="dispatch")
@method_decorator(user_is_employer, name="dispatch")
class SendResponseView(UpdateView):
    model = Applicant
    http_method_names = ["post"]
    pk_url_kwarg = "applicant_id"
    fields = ("status", "comment")

    def get_success_url(self):
        job_id = self.request.POST.get("job_id") or self.get_object().job.id
        return reverse_lazy(
            "jobsapp:applied-applicant-view",
            kwargs={"job_id": job_id, "applicant_id": self.get_object().id},
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            old_status = self.object.status
            new_status = int(form.cleaned_data["status"])

            if old_status != new_status:
                self.object.status = new_status
                self.object.comment = form.cleaned_data.get("comment", "")
                self.object.save()
                
                status_map = {1: "Pending", 2: "Accepted", 3: "Rejected"}
                status_text = status_map.get(new_status, "Unknown")
                messages.success(self.request, f"Response was successfully sent. Status changed to {status_text}.")
            else:
                messages.warning(self.request, "Response already sent with the same status.")
        else:
            messages.error(request, "Error in updating response. Please correct the form errors.")
            return HttpResponseRedirect(self.get_success_url())

        return HttpResponseRedirect(self.get_success_url())


# --- Employer Profile Edit View ---
@method_decorator(login_required(login_url=reverse_lazy("accounts:login")), name="dispatch")
@method_decorator(user_is_employer, name="dispatch")
class EmployerProfileEditView(UpdateView):
    form_class = EmployerProfileUpdateForm
    context_object_name = "employer"
    template_name = "jobs/employer/edit-profile.html"
    success_url = reverse_lazy("accounts:employer-profile-update")

    @method_decorator(login_required(login_url=reverse_lazy("accounts:login")))
    @method_decorator(user_is_employer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = self.request.user
        if obj is None:
            raise Http404("User doesn't exist.")
        return obj

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully.")
        return super().form_valid(form)
