from django.db import models
from django.contrib.auth.models import User

TERM = (
    ('First Term', 'First Term'),
    ('Second Term', 'Second Term'),
    ('Third Term', 'Third Term'),
)

CLASSES = (
    ('JSS 1', 'JSS 1'),
    ('JSS 2', 'JSS 2'),
    ('JSS 3', 'JSS 3'),
    ('SSS 1', 'SSS 1'),
    ('SSS 2', 'SSS 2'),
    ('SSS 3', 'SSS 3'),
)

CLASS_ARM = (
    ('Gold', 'Gold'),
    ('Silver', 'Silver'),
)

# Create your models here.
class SchoolSession(models.Model):
    session_term = models.CharField(choices=TERM, max_length=11)
    session_year = models.CharField(max_length=20, default="2023/2024")
    start_date = models.DateField()
    end_date = models.DateField()
    number_of_time_school_opened = models.PositiveIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.session_term} {self.session_year} session"

class SchoolHoliday(models.Model):
    session = models.ForeignKey(SchoolSession, on_delete=models.CASCADE)
    about = models.TextField()
    start_date = models.DateField()
    resumption_date = models.DateField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.session.session_term} {self.session.session_year} holiday"
    
class ClassRoom(models.Model):
    class_room_name = models.CharField(max_length=5, choices=CLASSES)
    class_arm = models.CharField(max_length=6, choices=CLASS_ARM, default="Gold")
    session = models.ForeignKey(SchoolSession, on_delete=models.CASCADE)
    class_administrator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.class_room_name} {self.class_arm} for {self.session}"

class Subject(models.Model):
    subject_name = models.CharField(max_length=50)
    subject_teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    subject_description = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject_name} for {self.class_room}"
