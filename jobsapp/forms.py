# D:\django-job-portal-master\jobsapp\forms.py

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Job, Applicant
from tags.models import Tag
from jobs.models import Company


class CreateJobForm(forms.ModelForm):
    skills_input = forms.CharField(
        label="Skills (comma-separated)",
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g., Python, Django, SQL'})
    )
    
    # Add fields for company details that will update the employer's company
    company_name = forms.CharField(label="Company Name", max_length=255, required=True)
    company_description = forms.CharField(label="Company Description", widget=forms.Textarea, required=False)
    website = forms.URLField(label="Website", required=False)

    # <<< FIX: Explicitly add apply_url field to the form >>>
    apply_url = forms.URLField(label="Apply URL (users will apply on your website)", required=False)


    class Meta:
        model = Job
        # Exclude 'company' ForeignKey here, as it's handled manually in the view.
        # Also ensure other fields like 'user', 'created_at', 'tags' are excluded.
        # 'apply_url' is now explicitly added above, so remove it from exclude if it was there.
        exclude = ("user", "created_at", "tags", "company")
        labels = {
            "last_date": "Last Date",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If editing an existing job, pre-populate the skills_input field
        if self.instance and self.instance.pk:
            self.fields['skills_input'].initial = ", ".join([tag.name for tag in self.instance.tags.all()])
            
            # Pre-populate company details if the job is linked to a company
            if self.instance.company:
                self.fields['company_name'].initial = self.instance.company.name
                self.fields['company_description'].initial = self.instance.company.description
                self.fields['website'].initial = self.instance.company.website
            
            # Pre-populate apply_url if it exists on the job instance
            if self.instance.apply_url: # Check if instance has apply_url
                self.fields['apply_url'].initial = self.instance.apply_url


        # Add CSS classes to widgets in __init__
        self.fields['category'].widget.attrs.update({'class': 'form-control select2'})
        self.fields['type'].widget.attrs.update({'class': 'form-control select2'})
        self.fields['company_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['company_description'].widget.attrs.update({'class': 'form-control'})
        self.fields['website'].widget.attrs.update({'class': 'form-control'})
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['location'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_date'].widget.attrs.update({'class': 'form-control'}) # For validity date input
        self.fields['vacancy'].widget.attrs.update({'class': 'form-control'})
        self.fields['salary'].widget.attrs.update({'class': 'form-control'})
        
        # <<< FIX: Add class for apply_url field's widget >>>
        self.fields['apply_url'].widget.attrs.update({'class': 'form-control'})


    def clean_last_date(self):
        date = self.cleaned_data["last_date"]
        if date and date < timezone.now().date():
            raise ValidationError("Last date can't be before today.")
        return date

    def clean_skills_input(self):
        skills_string = self.cleaned_data.get("skills_input")
        if skills_string:
            skill_names = [s.strip() for s in skills_string.split(',') if s.strip()]
            if len(skill_names) > 6:
                raise forms.ValidationError("You can't add more than 6 skills.")
        return skills_string

    def save(self, commit=True, user=None):
        job = super().save(commit=False)

        # Assign the user (employer) if provided
        if user:
            job.user = user

        # The 'company' ForeignKey will be assigned in the view (JobCreateView.form_valid)
        # as it depends on the request.user.
        
        # Assign apply_url from form's cleaned data
        job.apply_url = self.cleaned_data.get('apply_url') # Assign apply_url to job instance

        if commit:
            job.save() # Save the job to the database to get an ID

            # Process the skills_input and set the tags
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
                job.tags.clear() # If no skills provided, clear existing tags for the job

        return job


class ApplyJobForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ("job",)
