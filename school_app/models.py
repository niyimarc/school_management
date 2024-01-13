from django.db import models
from django.contrib.auth.models import User
from user_profile.models import Profile
from school_setting.models import ClassRoom, Subject

# Create your models here.
class StudentProfile(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE)
    admission_date = models.DateField()
    current_class = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student.user
    
class TeacherProfile(models.Model):
    teacher = models.ForeignKey(Profile, on_delete=models.CASCADE)
    employed_date = models.DateField()
    subject = models.ManyToManyField(Subject)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.teacher.user
    
class ParentProfile(models.Model):
    parent = models.ForeignKey(Profile, on_delete=models.CASCADE)
    children = models.ManyToManyField(Profile, related_name="parent_children")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.parent.user