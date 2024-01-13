from django.contrib.auth.models import User
from .models import Profile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
import os
from dotenv import load_dotenv
load_dotenv()
get_from_email = os.environ.get('EMAIL_HOST_USER')
business_name = os.environ.get('BUSINESS_NAME')
business_logo = os.environ.get('BUSINESS_LOGO')
contact_email = os.environ.get('CONTACT_EMAIL')
from_email = business_name + "<" + get_from_email + ">"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    profile, _ = Profile.objects.get_or_create(user=instance)
    
    # Explicitly set the verification_token for new profiles
    if created:
        profile.verification_token = profile.generate_verification_token()
        profile.save()

    if created or profile.email_verified is False and profile.user.email is not None:
        send_email_verification(profile, new_email=instance.email)
    
    # If the user is updated, save the profile
    elif not created:
        instance.profile.save()



def send_email_verification(profile, new_email=None):
    user_name = profile.user.username
    verification_url = profile.get_verification_url()
    base_url = settings.BASE_URL.rstrip('/')
    verification_url = f"{base_url}{verification_url}"

    title = 'Verify your email'
    context = {
        'user_name': user_name,
        'verification_url': verification_url,
        'business_name': business_name,
        'contact_email': contact_email,
        'title': title,
        'business_logo': business_logo,
        'base_url': base_url,
    }
    html_message = render_to_string('school_app/email_templates/verification_email.html', context)
    details = f"Hi {user_name} Click the link below to verify your email {verification_url}"
    to_email = new_email or profile.user.email 
    send_mail(
            title,
            details,
            from_email,
            [to_email],
            fail_silently=False,
            html_message=html_message,
        )

def send_password_reset_email(user, profile, token):
    base_url = settings.BASE_URL.rstrip('/')
    reset_link = profile.get_password_reset_token_url()
    reset_link = f"{base_url}{reset_link}"
    title = 'Password Reset'
    context = {
        'user_name': user,
        'reset_link': reset_link,
        'business_name': business_name,
        'contact_email': contact_email,
        'title': title,
        'business_logo': business_logo,
        'base_url': base_url,
    }
    html_message = render_to_string('school_app/email_templates/password_reset.html', context)
    details = f'Click the following link to reset your password: {reset_link}'
    send_mail(
        title,
        details,
        from_email,
        [user.email],
        fail_silently=False,
        html_message=html_message,
    )    