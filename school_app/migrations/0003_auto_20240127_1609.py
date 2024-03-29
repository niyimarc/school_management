# Generated by Django 3.2.23 on 2024-01-28 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school_app', '0002_assignment_continuousassesment_examination_studentassignmentscore_studentcontinuousassesmentscore_st'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentassignmentscore',
            name='student_total_score',
        ),
        migrations.RemoveField(
            model_name='studentcontinuousassesmentscore',
            name='student_total_score',
        ),
        migrations.RemoveField(
            model_name='studentexaminationscore',
            name='student_total_score',
        ),
        migrations.AlterField(
            model_name='studentcontinuousassesmentscore',
            name='obtainable_score',
            field=models.PositiveIntegerField(),
        ),
    ]
