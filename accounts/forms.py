# D:\django-job-portal-master\accounts\forms.py

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm 
from django.contrib.auth.forms import UserCreationForm as AuthUserCreationForm # Renamed to avoid clash

from django.utils.translation import gettext_lazy as _ 

from jobs.models import Company # Required for EmployerProfileForm to interact with Company model

User = get_user_model()

# Define GENDER_CHOICES directly in forms.py to avoid model loading issues
GENDER_CHOICES = (
    ('male', _('Male')),
    ('female', _('Female')),
    ('other', _('Other')),
    ('prefer_not_to_say', _('Prefer not to say')),
)


# --- Registration Forms (inheriting from forms.ModelForm) ---

class RegisterEmployeeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label=_("Confirm Password"))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'gender') 
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            self.add_error('password2', _("Passwords don't match"))
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"]) # Hash the password
        user.role = 'employee'
        user.username = self.cleaned_data['email'] # Assign email to username field
        if commit:
            user.save()
        return user


class RegisterEmployerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label=_("Confirm Password"))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email') 
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            self.add_error('password2', _("Passwords don't match"))
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"]) # Hash the password
        user.role = 'employer'
        user.username = self.cleaned_data['email'] # Assign email to username field
        if commit:
            user.save()
        return user


# --- Authentication Form ---
class LoginAuthenticationForm(AuthenticationForm): 
    username = forms.CharField(
        label=_("Email"),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'})
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )


# --- Admin-Specific Forms for CustomUser ---
class CustomUserCreationForm(AuthUserCreationForm): # Inherits from Django's UserCreationForm
    class Meta(AuthUserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name', 'gender', 'role', 'is_company', 'is_admin',)
        field_classes = {'username': forms.CharField} 

    def clean_username(self):
        username = self.cleaned_data['username']
        if self._meta.model.objects.filter(username=username).exists():
            raise forms.ValidationError(_("A user with that username already exists."))
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        if not user.username:
            user.username = user.email 
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm): # Inherits from Django's UserChangeForm
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name', 'gender', 'role', 'is_company', 'is_admin', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['readonly'] = True


# --- Employee Profile Update Form (for regular users) ---
class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = User 
        fields = ['first_name', 'last_name', 'gender'] 
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}), 
        }


# --- Employer Profile Update Form (for regular users, not admin) ---
class EmployerProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    company_name = forms.CharField(label="Company Name", max_length=255, required=True, 
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    company_description = forms.CharField(label="Company Description", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}), required=False)
    website = forms.URLField(label="Company Website", required=False, 
                             widget=forms.URLInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email'] 
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'readonly': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.role == 'employer':
            if hasattr(self.instance, 'company_profile') and self.instance.company_profile: 
                company = self.instance.company_profile 
                self.fields['company_name'].initial = company.name
                self.fields['company_description'].initial = company.description
                self.fields['website'].initial = company.website
            else: 
                self.fields['company_name'].initial = ''
                self.fields['company_description'].initial = ''
                self.fields['website'].initial = ''
        
        self.fields['email'].widget.attrs.update({'class': 'form-control'})


    def save(self, commit=True):
        user = super().save(commit=False)
        company_name = self.cleaned_data.pop('company_name')
        company_description = self.cleaned_data.pop('company_description')
        website = self.cleaned_data.pop('website')

        if commit:
            user.save() 
            
            company, created = Company.objects.get_or_create(user=user)
            company.name = company_name
            company.description = company_description
            company.website = website
            company.save() 
        return user

