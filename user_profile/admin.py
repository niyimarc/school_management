from django.contrib import admin
from .models import Profile
# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address', 'gender', 'dob', 'image', 'role', 'status', 'email_verified', 'is_verified', 'is_active')
    readonly_fields = ('user', 'password_reset_token_is_used', 'email_verified', 'password_reset_token_created_on')
    list_filter = ('email_verified', 'is_verified', 'is_active') 
    
admin.site.register(Profile, ProfileAdmin)