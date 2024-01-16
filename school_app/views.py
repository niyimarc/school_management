from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required #this decorator allow only logged in user to view the page
def dashboard(request):
    return render(request, 'school_app/dashboard/index.html')