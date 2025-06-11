from django.contrib import admin
# <<< CORRECT: Import the MODEL classes from .models >>>
from .models import ResumeCv, ResumeCvCategory, ResumeCvTemplate 

# Register ResumeCvCategory with a custom ModelAdmin
@admin.register(ResumeCvCategory)
class ResumeCvCategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the ResumeCvCategory model.
    Defines how ResumeCvCategory objects are displayed and managed in the Django admin.
    """
    list_display = ('name', 'color', 'created_at', 'updated_at')
    search_fields = ('name',)
    fields = ('name', 'thumbnail', 'color',)

# Register ResumeCvTemplate with a custom ModelAdmin
@admin.register(ResumeCvTemplate)
class ResumeCvTemplateAdmin(admin.ModelAdmin):
    """
    Admin configuration for the ResumeCvTemplate model.
    Ensures all fields are visible and manageable for resume templates.
    """
    list_display = ('name', 'category', 'active', 'is_premium', 'created_at', 'updated_at')
    search_fields = ('name', 'category__name') 
    list_filter = ('active', 'is_premium', 'category')
    fields = ('name', 'category', 'thumbnail', 'content', 'style', 'active', 'is_premium')
    raw_id_fields = ('category',)

# Register ResumeCv with a custom ModelAdmin
@admin.register(ResumeCv)
class ResumeCvAdmin(admin.ModelAdmin):
    """
    Admin configuration for the ResumeCv model.
    Manages individual user resumes in the Django admin.
    """
    list_display = ('user', 'template', 'name', 'is_published', 'view_count', 'created_at')
    search_fields = ('name', 'user__email', 'template__name') 
    list_filter = ('is_published', 'template', 'user')
    fields = ('user', 'template', 'name', 'content', 'style', 'is_published', 'view_count')
    raw_id_fields = ('user', 'template',)
    readonly_fields = ('code', 'view_count',)
