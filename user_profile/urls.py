from django.urls import path
from user_profile import views

app_name = 'user_profile'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('verify_email/<str:token>', views.verify_email, name='verify_email'),
    path('register/', views.register, name='register'),
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/reset/<uidb64>/<token>/', views.CustomSetPasswordView.as_view(), name='set_password'),
    path('forget_password_done/', views.CustomPasswordResetDoneView.as_view(), name='forget_password_done'),
]