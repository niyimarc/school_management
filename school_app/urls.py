from django.urls import path
from school_app import views
from django.contrib.auth import views as auth_views

app_name = 'school_app'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('logout/', auth_views.LogoutView.as_view(next_page='user_profile:login'), name='logout'),
]