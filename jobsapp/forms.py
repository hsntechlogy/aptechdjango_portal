# D:\django-job-portal-master\jobsapp\forms.py

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import Job, Applicant
from tags.models import Tag
from jobs.models import Company # Ensure Company is imported from the correct app


class CreateJobForm(forms.ModelForm):
    skills_input = forms.CharField(
        label=_("Skills (comma-separated)"),
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('e.g., Python, Django, SQL')})
    )
    
    # Fields for company details that will be saved/updated via the employer's Company model
    company_name = forms.CharField(label=_("Company Name"), max_length=255, required=True)
    company_description = forms.CharField(label=_("Company Description"), widget=forms.Textarea, required=False)
    website = forms.URLField(label=_("Website"), required=False)

    apply_url = forms.URLField(label=_("Apply URL (users will apply on your website)"), required=False)


    class Meta:
        model = Job
        # Exclude 'user', 'created_at', 'tags', 'company' as they are handled manually in the view or auto
        # 'apply_url' is a model field, so it should NOT be in exclude if you want it to be part of the form's data handling.
        exclude = ("user", "created_at", "tags", "company", "is_published", "filled") # Exclude is_published and filled too if managed elsewhere
        labels = {
            "last_date": _("Last Date"),
            "type": _("Job Type"), 
            "category": _("Category"), 
            "title": _("Job Title"),
            "location": _("Location"),
            "description": _("Description"),
            "vacancy": _("Vacancy"),
            "salary": _("Salary"),
        }
        widgets = {
            'last_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), 
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # If editing an existing job, pre-populate fields
        if self.instance and self.instance.pk:
            self.fields['skills_input'].initial = ", ".join([tag.name for tag in self.instance.tags.all()])
            
            if self.instance.company:
                self.fields['company_name'].initial = self.instance.company.name
                self.fields['company_description'].initial = self.instance.company.description
                self.fields['website'].initial = self.instance.company.website
            
            if self.instance.apply_url: 
                self.fields['apply_url'].initial = self.instance.apply_url


        # Add consistent CSS classes to other form fields
        common_attrs = {'class': 'form-control'}
        self.fields['category'].widget.attrs.update({'class': 'form-control select2'}) # Assuming select2 for category
        self.fields['type'].widget.attrs.update({'class': 'form-control select2'}) # Assuming select2 for type
        self.fields['company_name'].widget.attrs.update(common_attrs)
        self.fields['company_description'].widget.attrs.update(common_attrs)
        self.fields['website'].widget.attrs.update(common_attrs)
        self.fields['title'].widget.attrs.update(common_attrs)
        self.fields['location'].widget.attrs.update(common_attrs)
        self.fields['vacancy'].widget.attrs.update(common_attrs)
        self.fields['salary'].widget.attrs.update(common_attrs)
        self.fields['apply_url'].widget.attrs.update(common_attrs)


    def clean_last_date(self):
        date = self.cleaned_data["last_date"]
        if date and date < timezone.now().date():
            raise ValidationError(_("Last date can't be before today."))
        return date

    def clean_skills_input(self):
        skills_string = self.cleaned_data.get("skills_input")
        if skills_string:
            skill_names = [s.strip() for s in skills_string.split(',') if s.strip()]
            if len(skill_names) > 6:
                raise forms.ValidationError(_("You can't add more than 6 skills."))
        return skills_string

    def save(self, commit=True, user=None):
        job = super().save(commit=False)

        if user:
            job.user = user
        
        job.apply_url = self.cleaned_data.get('apply_url') # Assign apply_url to job instance

        if commit:
            job.save() 
            
            skills_string = self.cleaned_data.get("skills_input")
            if skills_string:
                skill_names = [s.strip() for s in skills_string.split(',') if s.strip()]
                tags_to_add = []
                for skill_name in skill_names:
                    tag, created = Tag.objects.get_or_create(
                        name__iexact=skill_name,
                        defaults={'name': skill_name}
                    )
                    tags_to_add.append(tag)
                job.tags.set(tags_to_add)
            else:
                job.tags.clear() 

        return job


class ApplyJobForm(forms.ModelForm):
    cv = forms.FileField(label=_("Upload your Resume/CV (PDF, DOCX)"), required=True,
                         help_text=_("Accepted formats: PDF, DOCX (max 5MB)."))

    class Meta:
        model = Applicant
        fields = ("cv",) 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cv'].widget.attrs.update({'class': 'form-control-file'})

    def clean_cv(self):
        cv_file = self.cleaned_data.get('cv')
        if cv_file:
            allowed_types = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
            if cv_file.content_type not in allowed_types:
                raise ValidationError(_("Only PDF and DOCX files are allowed."))
            
            if cv_file.size > 5 * 1024 * 1024: 
                raise ValidationError(_("File size cannot exceed 5MB."))
        return cv_file

