# Generated by Django 4.2.4 on 2024-07-16 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licence', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='license',
            name='country_of_issue',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='license',
            name='license_class',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
