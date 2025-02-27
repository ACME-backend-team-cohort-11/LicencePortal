# Generated by Django 4.2.4 on 2024-07-16 14:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('application', '0002_licenseapplication_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='licenseapplication',
            name='appointment_date',
        ),
        migrations.RemoveField(
            model_name='licenseapplication',
            name='appointment_day',
        ),
        migrations.RemoveField(
            model_name='licenseapplication',
            name='appointment_time',
        ),
        migrations.RemoveField(
            model_name='licenseapplication',
            name='date_of_issuance',
        ),
        migrations.RemoveField(
            model_name='licenseapplication',
            name='date_of_reissuance',
        ),
        migrations.RemoveField(
            model_name='licenseapplication',
            name='date_of_renewal',
        ),
        migrations.RemoveField(
            model_name='licenseapplication',
            name='user',
        ),
        migrations.AlterField(
            model_name='licenseapplication',
            name='applicant',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
