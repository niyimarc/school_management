from django.db import models
from django.contrib.auth.models import User
from user_profile.models import Profile
from school_setting.models import ClassRoom, Subject
from django.core.exceptions import ValidationError

CA = (
    ('Test', 'Test'),
    ('Class Work', 'Class Work'),
)

STATUS = (
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
)

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
    

class ContinuousAssesment(models.Model):
    ca_type = models.CharField(max_length=10, choices=CA)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    maximum_score = models.PositiveIntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject} {self.ca_type} for {self.subject.class_room.class_room_name} on {self.created_on}"

class StudentContinuousAssesmentScore(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    ca = models.ForeignKey(ContinuousAssesment, on_delete=models.CASCADE, verbose_name="Continous Assesment")
    student_score = models.PositiveIntegerField(default=0)
    obtainable_score = models.PositiveIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.obtainable_score:
            if self.student_score > self.ca.maximum_score:
                raise ValidationError("Student score cannot be more than the Obtainable score.")
            self.obtainable_score = self.ca.maximum_score
        super().save(*args, **kwargs)

class Assignment(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    maximum_score = models.PositiveIntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject} Assignment for {self.subject.class_room.class_room_name} on {self.created_on}"

class StudentAssignmentScore(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, verbose_name="Assignment")
    student_score = models.PositiveIntegerField()
    obtainable_score = models.PositiveIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.obtainable_score:
            if self.student_score > self.assignment.maximum_score:
                raise ValidationError("Student score cannot be more than the Obtainable score.")
            self.obtainable_score = self.assignment.maximum_score
        super().save(*args, **kwargs)


class Examination(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    maximum_score = models.PositiveIntegerField(default=60)
    exam_date = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject}"

class StudentExaminationScore(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Examination, on_delete=models.CASCADE)
    student_score = models.PositiveIntegerField(default=0)
    obtainable_score = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=8, choices=STATUS)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.obtainable_score:
            if self.student_score > self.exam.maximum_score:
                raise ValidationError("Student score cannot be more than the Obtainable score.")
            self.obtainable_score = self.exam.maximum_score
        super().save(*args, **kwargs)

class StudentTotalGrade(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    ca_score = models.PositiveIntegerField(default=0)
    exam_score = models.PositiveIntegerField(default=0)
    total_score = models.PositiveIntegerField(default=0)
    student_grade = models.CharField(max_length=3, default="Nil")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.total_score = self.ca_score + self.exam_score
        if self.total_score >= 75:
            self.student_grade = "A"
        elif self.total_score >= 65:
            self.student_grade = "B"
        elif self.total_score >= 55:
            self.student_grade = "C"
        elif self.total_score >= 50:
            self.student_grade = "D"
        elif self.total_score >= 40:
            self.student_grade = "E"
        else:
            self.student_grade = "F"
        super().save(*args, **kwargs)