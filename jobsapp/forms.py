# D:\django-job-portal-master\jobsapp\forms.py

from django import forms
from django.utils.translation import gettext_lazy as _
from jobsapp.models import Job, Applicant # Make sure Applicant is imported
from tags.models import Tag # Assuming Tag model is in tags.models
from jobs.models import Company # Assuming Company model is in jobs.models
from tinymce.widgets import TinyMCE # Import TinyMCE

class CreateJobForm(forms.ModelForm):
    # These fields will be used to create/update the associated Company instance
    company_name = forms.CharField(label=_("Company Name"), max_length=255, required=True, 
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    company_description = forms.CharField(label=_("Company Description"), widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}), required=False)
    website = forms.URLField(label=_("Company Website"), required=False, 
                             widget=forms.URLInput(attrs={'class': 'form-control'}))

    # A field to handle comma-separated tags, not directly mapped to a model field
    skills_input = forms.CharField(
        label=_("Skills (comma-separated)"),
        max_length=500,
        required=False,
        help_text=_("Enter comma-separated skills (e.g., Python, Django, REST API)."),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Job
        # Exclude 'company' field as we are handling it separately with company_name, company_description, website
        # Also exclude 'user', 'is_published', 'filled' as they are set programmatically
        # Note: 'salary' is a single field here, 'gender' is removed.
        fields = [
            'title', 'description', 'location', 'category', 'job_type', 
            'vacancy', 'salary', 'experience', 'last_date', 'apply_url',
            # Custom fields to be handled in the view
            'company_name', 'company_description', 'website', 'skills_input', 
           
        ]
        # Map model fields to Bootstrap-friendly form controls and TinyMCE
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title'}),
            'description': TinyMCE(attrs={'cols': 80, 'rows': 15, 'placeholder': 'Detailed job description', 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., New York, Remote'}),
            'category': forms.Select(attrs={'class': 'form-control'}), 
            'job_type': forms.Select(attrs={'class': 'form-control'}), 
            'vacancy': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 50000'}), # Single salary field
            'experience': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2-5 years'}),
            'last_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'apply_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com/apply'}),
            # Tags will be handled by skills_input, but if you used MTM field directly, you'd use SelectMultiple + select2
            # 'tags': forms.SelectMultiple(attrs={'class': 'form-control select2'}), # Example if tags was a direct MTM
        }
        labels = {
            'salary': _('Salary ($)'), # Updated label for single salary field
            'is_published': _('Publish Immediately'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add 'form-control' class to all direct fields for consistent styling
        for field_name, field in self.fields.items():
            if field_name not in ['description', 'company_description', 'skills_input'] and not isinstance(field.widget, (forms.Select, TinyMCE)):
                if 'class' in field.widget.attrs:
                    field.widget.attrs['class'] += ' form-control'
                else:
                    field.widget.attrs['class'] = 'form-control'

        # Populate initial values for company fields when updating an existing Job
        if self.instance and self.instance.pk:
            if self.instance.company:
                self.fields['company_name'].initial = self.instance.company.name
                self.fields['company_description'].initial = self.instance.company.description
                self.fields['website'].initial = self.instance.company.website
            
            # Populate initial values for skills_input from Job's many-to-many tags
            if self.instance.tags.exists():
                self.fields['skills_input'].initial = ", ".join([tag.name for tag in self.instance.tags.all()])

    def clean_skills_input(self):
        # This method is called to clean the 'skills_input' field
        skills_string = self.cleaned_data.get('skills_input', '')
        if not skills_string:
            return []
        # Split by comma, strip whitespace, remove empty strings
        skills_list = [s.strip() for s in skills_string.split(',') if s.strip()]
        return skills_list

    def save(self, commit=True):
        # The 'company_name', 'company_description', 'website' and 'skills_input'
        # are handled in the view (JobCreateView/JobUpdateView) before calling form.save()
        # They are popped from cleaned_data in the view, so they won't be here.

        job = super().save(commit=commit) # Save the Job instance (without M2M for now)

        if commit: # Only process tags if commit is True
            skills_data = self.cleaned_data.get('skills_input', []) # Retrieve the cleaned data
            tag_objects = []
            for skill_name in skills_data:
                # Use slugify for slug generation if it's not handled automatically by a signal
                tag, created = Tag.objects.get_or_create(name=skill_name, defaults={'slug': skill_name.lower().replace(' ', '-')})
                tag_objects.append(tag)
            job.tags.set(tag_objects) # Set the many-to-many relationship
        
        return job

class ApplyJobForm(forms.ModelForm):
    # This form is for applicants to upload their CV
    class Meta:
        model = Applicant
        fields = ['cv'] # Only CV field is needed for application
        widgets = {
            'cv': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
