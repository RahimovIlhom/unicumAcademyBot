# Generated by Django 5.1.1 on 2024-09-19 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='a',
            field=models.CharField(max_length=255, verbose_name='Correct answer'),
        ),
    ]
