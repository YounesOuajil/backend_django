# Generated by Django 5.0.4 on 2024-04-25 13:19

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0012_recruiter_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
