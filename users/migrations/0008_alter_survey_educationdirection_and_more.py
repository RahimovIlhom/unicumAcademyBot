# Generated by Django 5.0 on 2024-10-11 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_survey_coursetype_alter_survey_englishlevel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='educationDirection',
            field=models.CharField(blank=True, choices=[('software_engineering', 'Software Engineering'), ('computer_engineering', 'Computer Engineering'), ('banking', 'Banking'), ('finance_and_financial_technologies', 'Finance and Financial Technologies'), ('logistics', 'Logistics'), ('economics', 'Economics'), ('accounting', 'Accounting'), ('tourism_and_hospitality', 'Tourism and Hospitality'), ('preschool_education', 'Preschool Education'), ('primary_education', 'Primary Education'), ('special_pedagogy', 'Special Pedagogy'), ('native_language_and_literature', 'Native Language and Literature'), ('foreign_language_and_literature', 'Foreign Language and Literature'), ('history', 'History'), ('mathematics', 'Mathematics'), ('psychology', 'Psychology'), ('architecture', 'Architecture'), ('social_work', 'Social Work')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='educationType',
            field=models.CharField(blank=True, choices=[('daytime', 'Daytime'), ('evening', 'Evening'), ('externally', 'Externally')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='englishGoal',
            field=models.CharField(blank=True, choices=[('career', 'Good career'), ('knowledge', 'Acquiring knowledge'), ('abroad', 'Work or study abroad'), ('entertainment', 'Understand movies/music'), ('certificate', 'Get certificate for university')], max_length=20, null=True),
        ),
    ]
