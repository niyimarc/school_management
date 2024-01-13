# Generated by Django 3.2.23 on 2024-01-13 02:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=10, null=True, verbose_name='Phone Number')),
                ('address', models.CharField(blank=True, max_length=200, null=True, verbose_name='Home Address')),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], max_length=6, null=True)),
                ('dob', models.DateField(blank=True, null=True, verbose_name='Date of Birth')),
                ('role', models.CharField(blank=True, choices=[('Student', 'Student'), ('Parent', 'Parent'), ('Teacher', 'Teacher'), ('Administrator', 'Administrator')], max_length=13, null=True)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Graduated', 'Graduated'), ('Probation', 'Probation'), ('Suspended', 'Suspended'), ('Dismiss', 'Dismiss')], default='Inactive', max_length=9)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('email_verified', models.BooleanField(default=False)),
                ('verification_token', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('password_reset_token', models.UUIDField(blank=True, editable=False, null=True)),
                ('password_reset_token_is_used', models.BooleanField(default=True)),
                ('password_reset_token_created_on', models.DateTimeField(blank=True, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
