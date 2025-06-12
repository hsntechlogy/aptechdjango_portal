# D:\django-job-portal-master\accounts\views.py (COMPLETE FILE)

from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404 
from django.views.generic import CreateView, FormView, RedirectView, UpdateView, View 
from django.core.mail import send_mail
import random
from django.utils.decorators import method_decorator 
from .models import OTPVerification, CustomUser 
from django.conf import settings 
from django.contrib.auth.decorators import user_passes_test, login_required 
from notifications.models import Notification 
from django.contrib.auth.backends import ModelBackend 
from django.urls import reverse_lazy 
from django.utils import timezone 

# Corrected form import names to match accounts/forms.py
from accounts.forms import (
    RegisterEmployeeForm,      
    RegisterEmployerForm,      
    LoginAuthenticationForm,   
    EmployeeProfileForm, 
    EmployerProfileForm 
)


class RegisterEmployeeView(CreateView):
    model = CustomUser
    form_class = RegisterEmployeeForm 
    template_name = "accounts/register.html" 
    success_url = reverse_lazy('accounts:login') 

    extra_context = {"title": "Register as Employee"}

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.role == 'employee':
                return redirect('jobsapp:home')
            elif request.user.role == 'employer':
                return redirect('jobsapp:employer-dashboard')
            else:
                return redirect('admin:index') 
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False 
        user.save()

        otp_instance = OTPVerification.objects.create(user=user, otp_code=str(random.randint(100000, 999999)))
        send_mail(
            'Your OTP for Job Portal Registration',
            f'Your One-Time Password (OTP) is: {otp_instance.otp_code}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        messages.success(self.request, "Registration successful! Please check your email for OTP to activate your account.")
        return redirect('accounts:verify_otp_page', user_id=user.id) 

    def form_invalid(self, form):
        return render(self.request, self.template_name, {"form": form, "title": self.extra_context["title"]})


class RegisterEmployerView(CreateView):
    model = CustomUser
    form_class = RegisterEmployerForm 
    template_name = "accounts/register.html" 
    success_url = reverse_lazy('accounts:login') 

    extra_context = {"title": "Register as Employer"}

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.role == 'employee':
                return redirect('jobsapp:home')
            elif request.user.role == 'employer':
                return redirect('jobsapp:employer-dashboard')
            else:
                return redirect('admin:index') 
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False 
        user.save()

        otp_instance = OTPVerification.objects.create(user=user, otp_code=str(random.randint(100000, 999999)))
        send_mail(
            'Your OTP for Job Portal Registration',
            f'Your One-Time Password (OTP) is: {otp_instance.otp_code}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        messages.success(self.request, "Registration successful! Please check your email for OTP to activate your account.")
        return redirect('accounts:verify_otp_page', user_id=user.id) 

    def form_invalid(self, form):
        return render(self.request, self.template_name, {"form": form, "title": self.extra_context["title"]})


class LoginView(FormView):
    success_url = "/"
    form_class = LoginAuthenticationForm 
    template_name = "accounts/login.html"

    extra_context = {"title": "Login"}

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.role == 'employee':
                return redirect('jobsapp:home')
            elif self.request.user.role == 'employer':
                return redirect('jobsapp:employer-dashboard')
            elif self.request.user.is_staff or self.request.user.is_superuser:
                return redirect('admin:index')
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        if "next" in self.request.GET and self.request.GET["next"] != "":
            return self.request.GET["next"]
        else:
            if self.request.user.is_authenticated:
                if self.request.user.role == 'employee':
                    return reverse_lazy('jobsapp:home')
                elif self.request.user.role == 'employer':
                    return reverse_lazy('jobsapp:employer-dashboard')
                elif self.request.user.is_staff or self.request.user.is_superuser:
                    return reverse_lazy('admin:index')
            return reverse_lazy('jobsapp:home') 


    def form_valid(self, form):
        user = form.get_user()
        if not user.is_active:
            messages.error(self.request, "Please verify your account with OTP before logging in.")
            return redirect('accounts:verify_otp_page', user_id=user.pk)
        
        auth.login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(self.request, f"Welcome, {user.email}!")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class LogoutView(RedirectView):
    url = reverse_lazy("accounts:login") 

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, "You are now logged out.")
        return super(LogoutView, self).get(request, *args, **kwargs)


def send_otp_email(user):
    otp = str(random.randint(100000, 999999))
    OTPVerification.objects.update_or_create(user=user, defaults={'otp_code': otp, 'verified': False}) 
    send_mail(
        subject='Your OTP Code',
        message=f'Your OTP is {otp}',
        from_email=settings.DEFAULT_FROM_EMAIL, 
        recipient_list=[user.email],
        fail_silently=False,
    )


def verify_otp(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    if user.is_active:
        messages.success(request, "Your account is already active. Please log in.")
        return redirect('accounts:login')
    
    try:
        otp_record = OTPVerification.objects.get(user=user) 
    except OTPVerification.DoesNotExist:
        messages.error(request, "No pending OTP for this account or account already verified.")
        return redirect('accounts:login') 

    if request.method == "POST":
        code = request.POST.get("otp_code")
        if otp_record.otp_code == code:
            if (timezone.now() - otp_record.created_at).total_seconds() < 600: # OTP valid for 10 minutes
                user.is_active = True
                user.save()
                otp_record.delete() 
                messages.success(request, "Account activated successfully! You can now log in.")
                
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                
                if user.role == 'employee':
                    return redirect('jobsapp:home')
                elif user.role == 'employer':
                    return redirect('jobsapp:employer-dashboard')
                else: 
                    return redirect('admin:index') 
            else:
                messages.error(request, "OTP has expired. Please request a new one.")
                otp_record.delete() 
                return redirect('accounts:resend_otp', user_id=user.pk)
        else:
            messages.error(request, "Invalid OTP. Please try again.")
    
    return render(request, 'accounts/verify_otp.html', {'user': user})


def resend_otp(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    if user.is_active:
        messages.info(request, "Account already active.")
        return redirect('accounts:login')

    otp_code = str(random.randint(100000, 999999))
    OTPVerification.objects.update_or_create(user=user, defaults={'otp_code': otp_code, 'verified': False}) 

    messages.info(request, "A new OTP has been sent to your email.")
    return redirect('accounts:verify_otp_page', user_id=user.pk)

# --- Profile Update Views ---

@method_decorator(login_required(login_url=reverse_lazy("accounts:login")), name='dispatch')
class EditProfileView(UpdateView): 
    model = CustomUser
    form_class = EmployeeProfileForm
    template_name = 'accounts/employee_profile_update.html'
    
    def get_object(self, queryset=None):
        return self.request.user 

    def get_success_url(self):
        return reverse_lazy('accounts:employee-profile-update', kwargs={'pk': self.request.user.pk})

    def form_valid(self, form):
        messages.success(self.request, "Your profile has been updated successfully!")
        return super().form_valid(form)


@method_decorator(login_required(login_url=reverse_lazy("accounts:login")), name='dispatch')
class EmployerProfileEditView(UpdateView): 
    model = CustomUser
    form_class = EmployerProfileForm
    template_name = 'accounts/employer_profile_update.html'
    
    def get_object(self, queryset=None):
        return self.request.user 

    def get_success_url(self):
        return reverse_lazy('accounts:employer-profile-update', kwargs={'pk': self.request.user.pk})

    def form_valid(self, form):
        messages.success(self.request, "Your profile and company details have been updated successfully!")
        return super().form_valid(form)


# --- Admin Dashboard and Notifications (Original functions) ---
@user_passes_test(lambda u: u.is_admin) 
@login_required 
def admin_dashboard(request):
    return render(request, 'accounts/admin_dashboard.html') 


@login_required 
def notifications(request):
    notes = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/notifications.html', {'notifications': notes}) 


# --- Placeholder Error Handler Views ---
# These views are directly callable from jobs/urls.py (the ROOT_URLCONF)
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

