# Generated by Django 5.1.3 on 2025-06-14 12:13

import django.db.models.deletion
import resume_cv.models
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume_cv', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='resumecv',
            options={'verbose_name': 'Resume/CV', 'verbose_name_plural': 'Resumes/CVs'},
        ),
        migrations.AddField(
            model_name='resumecv',
            name='resume_file',
            field=models.FileField(blank=True, null=True, upload_to=resume_cv.models.resume_cv_directory_path),
        ),
        migrations.AlterField(
            model_name='resumecv',
            name='code',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='resumecv',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='resume_cvs', to='resume_cv.resumecvtemplate'),
        ),
    ]
