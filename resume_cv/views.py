# D:\django-job-portal-master\resume_cv\views.py

import json 
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseForbidden
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST


from jobsapp.decorators import user_is_employee
from jobsapp.mixins import EmployeeRequiredMixin

from resume_cv.forms import ResumeCvForm # Assuming this form now handles FileField
from resume_cv.models import ResumeCv # ResumeCvTemplate and ResumeCvCategory are not used by removed features


# --- REMOVED: TemplateListView class and related functions (resume_builder, update_builder, load_builder, update_template_choice) ---


class ResumeCVCreateView(LoginRequiredMixin, EmployeeRequiredMixin, View):
    """
    Handles creation of a resume, now primarily for file uploads.
    """
    form_class = ResumeCvForm
    template_name = "resumes/create_resume_upload.html" # A new template for the upload form

    def get(self, request, *args, **kwargs):
        """Displays the form for uploading a resume."""
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        """Processes the uploaded resume file."""
        f = self.form_class(request.POST, request.FILES) # request.FILES is crucial for file uploads
        if f.is_valid():
            r = f.save(commit=False)
            r.user = request.user
            # Ensure your ResumeCv model either allows 'template' to be null/blank
            # or you've removed the ForeignKey if templates are no longer relevant.
            # If the form provides a 'resume_file' field and saves it directly,
            # you might not need to set content/style here from a template.
            
            r.save() # Saves the resume instance, including the uploaded file (if form handles it)
            messages.success(request, "Resume uploaded successfully!")
            return redirect(reverse_lazy("resume_cv:resumes")) # Redirect to user's resume list
        else:
            print(f.errors) # Log form errors for debugging
            messages.error(request, f"Error uploading resume: {f.errors.as_text()}")
            # Re-render the form with errors if validation fails
            return render(request, self.template_name, {'form': f})


class UserResumeListView(ListView):
    model = ResumeCv
    template_name = "resumes/user_resumes.html"
    context_object_name = "resumes"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).order_by("-created_at")


@login_required
@user_is_employee
def download_resume(request, id):
    """
    Downloads a user's resume. Now primarily supports downloading uploaded files.
    """
    try:
        resume = get_object_or_404(ResumeCv, id=id, user=request.user)

        # Check for the new 'resume_file' field first
        if resume.resume_file: 
            # Serve the actual uploaded file
            pdf_content = resume.resume_file.read() # Correctly read from resume_file
            # Use content_type from the file if available, otherwise default to PDF
            content_type = resume.resume_file.file.content_type if hasattr(resume.resume_file.file, 'content_type') else "application/pdf"
            response = HttpResponse(pdf_content, content_type=content_type)
            response["Content-Disposition"] = f'attachment; filename="{resume.name or "resume"}.pdf"'
            return response
        else:
            # Fallback for old builder-generated content if still stored in content/style
            # This block can be removed entirely if all resumes are now file uploads
            if resume.content and resume.style:
                font_config = FontConfiguration()
                css_string = f"""
                    @font-face {{
                        font-family: "Font Awesome 5 Brands";
                        font-style: normal;
                        font-weight: 400;
                        src: url("{static('webfonts/fa-brands-400.eot')}");
                        src: url("{static('webfonts/fa-brands-400.eot?#iefix')}") format("embedded-opentype"),
                            url("{static('webfonts/fa-brands-400.woff2')}") format("woff2"),
                            url("{static('webfonts/fa-brands-400.woff')}") format("woff"),
                            url("{static('webfonts/fa-brands-400.ttf')}") format("truetype"),
                            url("{static('webfonts/fa-brands-400.svg#fontawesome')}") format("svg");
                    }}
                    @font-face {{
                        font-family: "Font Awesome 5 Free";
                        font-style: normal;
                        font-weight: 400;
                        src: url("{static('webfonts/fa-regular-400.eot')}");
                        src: url("{static('webfonts/fa-regular-400.eot?#iefix')}") format("embedded-opentype"),
                            url("{static('webfonts/fa-regular-400.woff2')}") format("woff2"),
                            url("{static('webfonts/fa-regular-400.woff')}") format("woff"),
                            url("{static('webfonts/fa-regular-400.ttf')}") format("truetype"),
                            url("{static('webfonts/fa-regular-400.svg#fontawesome')}") format("svg");
                    }}
                    @font-face {{
                        font-family: "Font Awesome 5 Free";
                        font-style: normal;
                        font-weight: 900;
                        src: url("{static('webfonts/fa-solid-900.eot')}");
                        src: url("{static('webfonts/fa-solid-900.eot?#iefix')}") format("embedded-opentype"),
                            url("{static('webfonts/fa-solid-900.woff2')}") format("woff2"),
                            url("{static('webfonts/fa-solid-900.woff')}") format("woff"),
                            url("{static('webfonts/fa-solid-900.ttf')}") format("truetype"),
                            url("{static('webfonts/fa-solid-900.svg#fontawesome')}") format("svg");
                    }}
                    .fa, .fas {{
                        font-family: "Font Awesome 5 Free";
                        font-weight: 900;
                        font-style: normal;
                    }}
                    .far {{
                        font-family: "Font Awesome 5 Free";
                        font-weight: 400;
                        font-style: normal;
                    }}
                    .fab {{
                        font-family: "Font Awesome 5 Brands";
                        font-weight: 400;
                        font-style: normal;
                    }}
                """
                combined_css_string = resume.style + "\n" + css_string
                css_stylesheet = CSS(string=combined_css_string, font_config=font_config)
                pdf_file = HTML(string=resume.content, encoding="utf-8").write_pdf(
                    stylesheets=[css_stylesheet], font_config=font_config
                )
                response = HttpResponse(pdf_file, content_type="application/pdf")
                response["Content-Disposition"] = f'attachment; filename="{resume.name or "resume"}.pdf"'
                return response
            else:
                # If no file and no content/style, then no resume to download
                messages.error(request, "Resume content or file not found for download.")
                return redirect(reverse_lazy("resume_cv:resumes"))

    except Http404:
        messages.error(request, "Resume not found or you do not have permission to download it.")
        return redirect(reverse_lazy("resume_cv:resumes"))
    except PermissionDenied:
        messages.error(request, "Permission denied to download this resume.")
        return redirect(reverse_lazy("resume_cv:resumes"))
    except Exception as e:
        messages.error(request, f"An error occurred while downloading the resume: {str(e)}")
        print(f"ERROR: Exception during download_resume: {e}") # Debugging
        return redirect(reverse_lazy("resume_cv:resumes"))
