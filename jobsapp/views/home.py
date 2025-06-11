from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, JsonResponse, HttpResponseNotAllowed
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView, TemplateView

# <<< ADD THIS LINE >>>
from django.shortcuts import render, redirect, get_object_or_404 

# Adjust imports based on your actual structure
from ..decorators import user_is_employee
from ..forms import ApplyJobForm
from ..models import Applicant, Favorite, Job
from jobs.models import Company, CompanyReview
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
        # q = JobDocument.search().query("match", title=self.request.GET['position']).to_queryset()
        # print(q)
        # return q
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
        obj = super(JobDetailsView, self).get_object(queryset=queryset)
        if obj is None:
            raise Http404("Job doesn't exists")
        return obj

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            # raise error
            raise Http404("Job doesn't exists")
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


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
            return HttpResponseRedirect(reverse_lazy("jobs:home"))

    def get_success_url(self):
        return reverse_lazy("jobs:jobs-detail", kwargs={"id": self.kwargs["job_id"]})

    # def get_form_kwargs(self):
    #     kwargs = super(ApplyJobView, self).get_form_kwargs()
    #     print(kwargs)
    #     kwargs['job'] = 1
    #     return kwargs

    def form_valid(self, form):
        # check if user already applied
        applicant = Applicant.objects.filter(user_id=self.request.user.id, job_id=self.kwargs["job_id"])
        if applicant:
            messages.info(self.request, "You already applied for this job")
            return HttpResponseRedirect(self.get_success_url())
        # save applicant
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


def favorite(request):
    if not request.user.is_authenticated:
        return JsonResponse(data={"auth": False, "status": "error"})

    job_id = request.POST.get("job_id")
    user_id = request.user.id
    try:
        fav = Favorite.objects.get(job_id=job_id, user_id=user_id, soft_deleted=False)
        if fav:
            fav.soft_deleted = True
            fav.save()
            return JsonResponse(
                data={"auth": True, "status": "removed", "message": "Job removed from your favorite list"}
            )
    except Favorite.DoesNotExist:
        Favorite.objects.create(job_id=job_id, user_id=user_id)
        return JsonResponse(data={"auth": True, "status": "added", "message": "Job added to your favorite list"})

# <<< Company Detail View >>>
class CompanyDetailView(DetailView):
    model = Company # Use the Company model from jobs.models
    template_name = 'jobs/company_details.html' # Path: templates/jobs/company_details.html
    context_object_name = 'company' # The object will be available as 'company' in the template
    pk_url_kwarg = 'pk' # Expects 'pk' from the URL pattern

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = self.get_object()
        context['jobs_by_company'] = company.jobs.filter(is_published=True).order_by('-created_at') # Get jobs posted by this company
        context['reviews'] = company.reviews.all().order_by('-created_at') # Get reviews for this company (using 'reviews' related_name)
        return context

# <<< The add_review view function >>>
# Assuming this is in jobsapp/views.py or jobsapp/views/home.py
# and imported in jobsapp/urls.py
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
        return redirect('jobs:company_detail', pk=company.id) # Redirect to the company's detail page

    return render(request, 'jobs/add_review.html', {'company': company})