from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
import uuid
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

GENDER =(
    ('Male', 'Male'),
    ('Female', 'Female'),
)

ROLE =(
    ('Student', 'Student'),
    ('Parent', 'Parent'),
    ('Teacher', 'Teacher'),
    ('Administrator', 'Administrator')
)

STATUS = (
    ('Active', 'Active'),
    ('Inactive', 'Inactive'),
    ('Graduated', 'Graduated'),
    ('Probation', 'Probation'),
    ('Suspended', 'Suspended'),
    ('Dismiss', 'Dismiss'),
)
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, verbose_name="Phone Number", null=True, blank=True)
    address = models.CharField(max_length=200, verbose_name="Home Address", null=True, blank=True)
    gender = models.CharField(choices=GENDER, null=True, blank=True, max_length=6)
    dob = models.DateField(verbose_name="Date of Birth", null=True, blank=True)
    image = models.ImageField(upload_to="profile_picture/", null=True, blank=True)
    role = models.CharField(max_length=13, choices=ROLE, null=True, blank=True)
    status = models.CharField(max_length=9, choices=STATUS, default="Inactive")
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    password_reset_token = models.UUIDField(editable=False, null=True, blank=True)
    password_reset_token_is_used = models.BooleanField(default=True)
    password_reset_token_created_on = models.DateTimeField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def generate_verification_token(self):
        if not self.verification_token:
            self.verification_token = uuid.uuid4()
        return str(self.verification_token)

    def get_verification_url(self):
        
        token = self.generate_verification_token()
        return reverse('user_profile:verify_email', kwargs={'token': token})
    
    def generate_password_reset_token(self):
        # Check if there's an existing token and if it's still valid
        if self.password_reset_token and self.is_password_reset_token_valid():
            return str(self.password_reset_token)
        self.password_reset_token = uuid.uuid4()
        self.password_reset_token_created_on = timezone.now()
        self.password_reset_token_is_used = False
        self.save()
        return str(self.password_reset_token)
    
    def get_password_reset_token_url(self):
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.id))
        token = self.generate_password_reset_token()
        return reverse('user_profile:set_password', kwargs={'uidb64': uidb64, 'token': token})
    
    def is_password_reset_token_valid(self):
        # Check if the password reset token is still valid
        if self.password_reset_token_created_on:
            expiration_time = self.password_reset_token_created_on + timedelta(minutes=15)
            return timezone.now() <= expiration_time
        return False

    def __str__(self):
        return self.user.username