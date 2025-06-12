from notifications.models import Notification  # ✅ import
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Company, CompanyReview

@login_required
def company_detail(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    error = None
    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")
        if rating and comment:
            review = CompanyReview.objects.create(
                company=company,
                user=request.user,
                rating=rating,
                comment=comment
            )
            # ✅ Create notification
            Notification.objects.create(
                user=request.user,
                message=f"Your review for {company.name} was submitted."
            )
            return redirect("company_detail", company_id=company.id)
        else:
            error = "All fields are required."

    reviews = company.companyreview_set.all()
    return render(request, "company/detail.html", {
        "company": company,
        "error": error,
        "reviews": reviews
    })

@login_required
def add_review(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    if request.method == 'POST':
        rating = request.POST['rating']
        comment = request.POST['comment']
        if rating and comment:
            CompanyReview.objects.create(
                company=company,
                user=request.user,
                rating=rating,
                comment=comment
            )
            Notification.objects.create(
                user=request.user,
                message=f"Your review for {company.name} was submitted."
            )
            return redirect('company_detail', company_id=company.id)
    return render(request, 'jobs/add_review.html', {'company': company})

from django.shortcuts import render, get_object_or_404
from .models import Company, CompanyReview

def company_list(request):
    companies = Company.objects.all()
    return render(request, 'jobs/company_list.html', {'companies': companies})

def company_detail(request, company_id):
    company = get_object_or_404(Company, pk=company_id)
    reviews = CompanyReview.objects.filter(company=company)
    return render(request, 'jobs/company_detail.html', {
        'company': company,
        'reviews': reviews
    })


# ... other views or code ...