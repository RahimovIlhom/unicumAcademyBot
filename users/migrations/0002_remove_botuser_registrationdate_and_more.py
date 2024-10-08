# Generated by Django 5.1.1 on 2024-09-19 09:54

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='botuser',
            name='registrationDate',
        ),
        migrations.RemoveField(
            model_name='botuser',
            name='updatedDate',
        ),
        migrations.AddField(
            model_name='botuser',
            name='registeredAt',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='botuser',
            name='updatedAt',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
