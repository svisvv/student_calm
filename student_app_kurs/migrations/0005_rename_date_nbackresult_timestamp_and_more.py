# Generated by Django 5.1.5 on 2025-05-30 00:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_app_kurs', '0004_rename_date_taken_schulteresult_timestamp_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nbackresult',
            old_name='date',
            new_name='timestamp',
        ),
        migrations.RenameField(
            model_name='testresult',
            old_name='timestamp',
            new_name='test_date',
        ),
        migrations.RemoveField(
            model_name='recommendation',
            name='resources',
        ),
        migrations.RemoveField(
            model_name='recommendation',
            name='score_range',
        ),
        migrations.RemoveField(
            model_name='testresult',
            name='test_name',
        ),
        migrations.AddField(
            model_name='testresult',
            name='test',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='student_app_kurs.test'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='nbackresult',
            name='correct_answers',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='BDIResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CPTResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct_hits', models.IntegerField(default=0)),
                ('false_alarms', models.IntegerField(default=0)),
                ('misses', models.IntegerField(default=0)),
                ('time_taken', models.FloatField(default=0.0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SpilbergerResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
