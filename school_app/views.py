from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from user_profile.models import Profile
from .models import StudentProfile
# Create your views here.

@login_required #this decorator allow only logged in user to view the page
def dashboard(request):
    user_profile = Profile.objects.get(user=request.user)
    context = {
        'active_user': request.user,
        'user_profile': user_profile,
    }
    return render(request, 'school_app/student_dashboard/index.html', context)