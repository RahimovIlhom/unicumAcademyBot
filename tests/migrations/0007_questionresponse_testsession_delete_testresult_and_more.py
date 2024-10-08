# Generated by Django 4.2 on 2024-09-22 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_botuser_options_alter_botuser_selectedlevel'),
        ('tests', '0006_alter_question_d'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(blank=True, max_length=1, null=True)),
                ('correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.question')),
            ],
            options={
                'db_table': 'question_responses',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='TestSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('beginner', 'Beginner'), ('elementary', 'Elementary'), ('pre-intermediate', 'Pre-Intermediate'), ('intermediate', 'Intermediate'), ('upper-intermediate', 'Upper-Intermediate'), ('advanced', 'Advanced'), ('proficient', 'Proficient')], max_length=20)),
                ('totalQuestions', models.IntegerField(default=20)),
                ('correctAnswers', models.IntegerField(default=0)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('completedAt', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.botuser')),
            ],
            options={
                'db_table': 'test_sessions',
                'ordering': ['-createdAt'],
            },
        ),
        migrations.DeleteModel(
            name='TestResult',
        ),
        migrations.AddField(
            model_name='questionresponse',
            name='test_session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_responses', to='tests.testsession'),
        ),
        migrations.AddField(
            model_name='questionresponse',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.botuser'),
        ),
    ]
