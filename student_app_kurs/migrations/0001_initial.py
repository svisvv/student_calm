# Generated by Django 5.1.3 on 2025-01-18 17:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('is_employed', models.BooleanField(default=False)),
                ('is_international', models.BooleanField(default=False)),
                ('is_nonresident', models.BooleanField(default=False)),
                ('is_freshman', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score_range', models.CharField(max_length=50)),
                ('text', models.TextField()),
                ('resources', models.TextField(blank=True, null=True)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_app_kurs.test')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField()),
                ('question_type', models.CharField(choices=[('single_choice', 'Single Choice'), ('multi_choice', 'Multi Choice'), ('open', 'Open')], max_length=20)),
                ('correct_answer', models.TextField(blank=True, null=True)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_app_kurs.test')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_date', models.DateTimeField()),
                ('score', models.DecimalField(decimal_places=2, max_digits=5)),
                ('hours_worked', models.IntegerField(default=0)),
                ('work_intensity', models.CharField(choices=[('none', 'None'), ('physical', 'Physical'), ('moderate', 'Moderate'), ('mental', 'Mental')], default='none', max_length=10)),
                ('follow_up_checked', models.BooleanField(default=False)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_app_kurs.test')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_app_kurs.user')),
            ],
        ),
        migrations.CreateModel(
            name='RecommendationTracking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completion_status', models.CharField(choices=[('completed', 'Completed'), ('partial', 'Partial'), ('not_completed', 'Not Completed')], max_length=20)),
                ('feedback', models.TextField(blank=True, null=True)),
                ('completion_date', models.DateTimeField(blank=True, null=True)),
                ('recommendation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_app_kurs.recommendation')),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_app_kurs.result')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_app_kurs.user')),
            ],
        ),
    ]
