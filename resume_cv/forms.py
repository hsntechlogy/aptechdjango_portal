# D:\django-job-portal-master\resume_cv\forms.py
from django import forms
from .models import ResumeCv

class ResumeCvForm(forms.ModelForm):
    # This form expects 'template' and 'name' as hidden inputs from templates.html
    # You might not need to explicitly list these fields if they are correctly
    # handled in the form_valid method of ResumeCVCreateView, but it's good practice
    # if you want to apply validation at the form level.
    class Meta:
        model = ResumeCv
        fields = ['template', 'name'] # Ensure these are the only fields you're passing directly from the form
        # The 'content' and 'style' fields are not usually passed from the initial form
        # they are populated by the builder.