from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import CreateView, FormView, RedirectView
from django.core.mail import send_mail
import random
from .models import OTPVerification, CustomUser
from accounts.forms import EmployeeRegistrationForm, EmployerRegistrationForm, UserLoginForm
from django.contrib.auth.decorators import user_passes_test
from notifications.models import Notification
from django.contrib.auth.backends import ModelBackend # Import ModelBackend

class RegisterEmployeeView(CreateView):
        model = CustomUser
        form_class = EmployeeRegistrationForm
        template_name = "accounts/employee/register.html"
        success_url = "/"

        extra_context = {"title": "Register"}

        def dispatch(self, request, *args, **kwargs):
            if request.user.is_authenticated:
                return HttpResponseRedirect(self.success_url)
            return super().dispatch(self.request, *args, **kwargs)

        def post(self, request, *args, **kwargs):
            form = self.form_class(data=request.POST)

            if form.is_valid():
                user = form.save(commit=False)
                password = form.cleaned_data.get("password1")
                user.set_password(password)
                user.save()

                send_otp_email(user)
                messages.info(request, "Registration successful! Please check your email for the OTP to activate your account.")
                return redirect('accounts:verify_otp_page', user_id=user.pk)
            else:
                return render(request, "accounts/employee/register.html", {"form": form})


class RegisterEmployerView(CreateView):
        model = CustomUser
        form_class = EmployerRegistrationForm
        template_name = "accounts/employer/register.html"
        success_url = "/"

        extra_context = {"title": "Register"}

        def dispatch(self, request, *args, **kwargs):
            if request.user.is_authenticated:
                return HttpResponseRedirect(self.success_url)
            return super().dispatch(self.request, *args, **kwargs)

        def post(self, request, *args, **kwargs):
            form = self.form_class(data=request.POST)

            if form.is_valid():
                user = form.save(commit=False)
                password = form.cleaned_data.get("password1")
                user.set_password(password)
                user.save()

                send_otp_email(user)
                messages.info(request, "Registration successful! Please check your email for the OTP to activate your account.")
                return redirect('accounts:verify_otp_page', user_id=user.pk)
            else:
                return render(request, "accounts/employer/register.html", {"form": form})


class LoginView(FormView):
        success_url = "/"
        form_class = UserLoginForm
        template_name = "accounts/login.html"

        extra_context = {"title": "Login"}

        def dispatch(self, request, *args, **kwargs):
            if self.request.user.is_authenticated:
                return HttpResponseRedirect(self.get_success_url())
            return super().dispatch(self.request, *args, **kwargs)

        def get_success_url(self):
            if "next" in self.request.GET and self.request.GET["next"] != "":
                return self.request.GET["next"]
            else:
                return self.success_url

        def get_form_class(self):
            return self.form_class

        def form_valid(self, form):
            user = form.get_user()
            if not user.is_active:
                messages.error(self.request, "Please verify your account with OTP before logging in.")
                return redirect('accounts:verify_otp_page', user_id=user.pk)
            
            auth.login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponseRedirect(self.get_success_url())

        def form_invalid(self, form):
            return self.render_to_response(self.get_context_data(form=form))


class LogoutView(RedirectView):
        url = "/login"

        def get(self, request, *args, **kwargs):
            auth.logout(request)
            messages.success(request, "You are now logged out")
            return super(LogoutView, self).get(request, *args, **kwargs)


def send_otp_email(user):
        otp = str(random.randint(100000, 999999))
        OTPVerification.objects.update_or_create(user=user, defaults={'otp_code': otp, 'verified': False})
        send_mail(
            subject='Your OTP Code',
            message=f'Your OTP is {otp}',
            from_email='no-reply@jobportal.com',
            recipient_list=[user.email],
        )
        print(f"DEBUG: Sent OTP {otp} to {user.email}")


def verify_otp(request, user_id):
        user = CustomUser.objects.get(pk=user_id)
        if user.is_active:
            messages.success(request, "Your account is already active. Please log in.")
            return redirect('accounts:login')
        
        try:
            otp_record = OTPVerification.objects.get(user=user, verified=False)
        except OTPVerification.DoesNotExist:
            messages.error(request, "No pending OTP for this account or account already verified.")
            return redirect('accounts:register')

        if request.method == "POST":
            code = request.POST.get("otp_code")
            if otp_record.otp_code == code:
                user.is_active = True
                user.save()
                otp_record.verified = True
                otp_record.save()
                messages.success(request, "Account activated successfully! You can now log in.")
                
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                
                return redirect('jobs:home')
            else:
                messages.error(request, "Invalid OTP. Please try again.")
        
        return render(request, 'accounts/verify_otp.html', {'user': user})


def resend_otp(request, user_id):
        user = CustomUser.objects.get(pk=user_id)
        if user.is_active:
            messages.info(request, "Account already active.")
            return redirect('accounts:login')

        OTPVerification.objects.filter(user=user, verified=False).delete()
        
        otp_code = str(random.randint(100000, 999999))
        OTPVerification.objects.create(user=user, otp_code=otp_code)

        print(f"DEBUG: Resending OTP {otp_code} to {user.email}")
        messages.info(request, "A new OTP has been sent to your email.")
        return redirect('accounts:verify_otp_page', user_id=user.pk)

@user_passes_test(lambda u: u.is_admin)
def admin_dashboard(request):
        return render(request, 'admin_dashboard.html')


def notifications(request):
        notes = Notification.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'notifications.html', {'notifications': notes})
    