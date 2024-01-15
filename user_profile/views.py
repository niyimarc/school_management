from django.shortcuts import render, get_object_or_404, redirect
from user_profile.forms import RegForm, CustomSetPasswordForm
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
import os
from dotenv import load_dotenv
load_dotenv()
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, LoginView
from .signals import send_password_reset_email
from django.utils.encoding import force_str as force_text
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse_lazy
from datetime import timedelta

get_from_email = os.environ.get('EMAIL_HOST_USER')

business_name = os.environ.get('BUSINESS_NAME')
contact_email = os.environ.get('CONTACT_EMAIL')

def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)

def login_excluded(redirect_to):
    """ This decorator kicks authenticated users out of a view """ 
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_to) 
            return view_method(request, *args, **kwargs)
        return _arguments_wrapper
    return _method_wrapper

class CustomLoginView(LoginView):
    template_name = 'school_app/auth/sign_in.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        # Your custom logic for successful login
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, 'Invalid login credentials. Please try again.')
        # Your custom logic for unsuccessful login
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_email'] = contact_email
        context['business_name'] = business_name
        return context



def register(request):
    if request.method == "POST":
        regform = RegForm(request.POST)
        if regform.is_valid():
            regform.save(commit=True)
            messages.success(request, 'Account Created successfully')
            return redirect("school_app:dashboard")
        else:
            # Iterate through form errors and add them to messages
            for field, errors in regform.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    else:
        regform = RegForm()
    return render(request, 'plans/auth/sign_up.html', {"regform": regform})

def verify_email(request, token):
    # Find the profile associated with the token
    profile = get_object_or_404(Profile, verification_token=token)

    # Update the email_verified field
    profile.email_verified = True
    profile.save()
    context = {
        'contact_email': contact_email,
        'business_name': business_name
    }
    return render(request, 'school_app/auth/verified_email.html', context)

# password reset request view 
class CustomPasswordResetView(PasswordResetView):
    template_name = 'school_app/auth/forget_password.html'
    success_url = reverse_lazy('user_profile:forget_password_done')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            profile = Profile.objects.get(user=user)
            # Check if the user has requested a reset within the last hour
            if profile.password_reset_token_created_on:
                last_request_time = profile.password_reset_token_created_on
                min_time_difference = timedelta(hours=5)
                remaining_time = timezone.now() - last_request_time
                if remaining_time < min_time_difference:
                    remaining_time_str = strfdelta(min_time_difference - remaining_time, "{hours}:{minutes:02d}:{seconds:02d}")
                    messages.error(self.request, f"Please wait {remaining_time_str} before requesting another password reset.")
                    return self.form_invalid(form)
        except User.DoesNotExist:
            messages.error(self.request, "The provided email does not exist.")
            return self.form_invalid(form)
        # Generate and save the password reset token to the profile
        token = profile.generate_password_reset_token()

        # Send password reset email
        send_password_reset_email(user, profile, token)

        return HttpResponseRedirect(self.get_success_url())
    
# password set view 
class CustomSetPasswordView(View):
    template_name = 'school_app/auth/set_password.html'

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(User, pk=int(uid))
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        # Pass the user to the form in the initial data
        form = CustomSetPasswordForm(user=user, initial={'user': user})
        return render(request, self.template_name, {'form': form, 'uidb64': uidb64, 'token': token})


    def post(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(User, pk=int(uid))
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        form = CustomSetPasswordForm(request.POST, user=user) 

        profile = Profile.objects.get(user=user)
        if not profile.is_password_reset_token_valid():
            messages.error(request, "Password reset token has expired.")
        elif profile.password_reset_token_is_used:
            messages.error(request, "You have used this token to reset your password.")
        else:
            if form.is_valid():
                form.save() 
                profile.password_reset_token_is_used = True
                profile.save()
                messages.success(request, "New password set successfully.")
                return redirect('user_profile:login')
            elif len(form.cleaned_data.get('new_password1')) < 8:
                messages.error(request, "Password must be at least 8 characters long.")
            else:
                messages.error(request, "Password not set.")
        return render(request, self.template_name, {'form': form, 'uidb64': uidb64, 'token': token})
    
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'school_app/auth/forget_password_done.html'