# Generated by Django 5.0 on 2024-10-12 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_survey_educationdirection_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='survey',
            table='surveys',
        ),
    ]