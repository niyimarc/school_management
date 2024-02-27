from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StudentContinuousAssesmentScore, StudentTotalGrade, StudentAssignmentScore, StudentExaminationScore, StudentProfile
from user_profile.models import Profile

@receiver(post_save, sender=StudentContinuousAssesmentScore)
def update_student_test_and_class_work_score_in_ca(sender, instance, created, **kwargs):
    if created:
        student_ca_score, created = StudentTotalGrade.objects.get_or_create(student=instance.student, subject=instance.ca.subject)
        student_ca_score.ca_score += instance.student_score
        student_ca_score.save()

@receiver(post_save, sender=StudentAssignmentScore)
def update_student_assignment_score_in_ca(sender, instance, created, **kwargs):
    if created:
        student_assignment_score, created = StudentTotalGrade.objects.get_or_create(student=instance.student, subject=instance.assignment.subject)
        student_assignment_score.ca_score += instance.student_score
        student_assignment_score.save()

@receiver(post_save, sender=StudentExaminationScore)
def update_student_exam_score_in_ca(sender, instance, created, **kwargs):
    if created:
        student_exam_score, created = StudentTotalGrade.objects.get_or_create(student=instance.student, subject=instance.exam.subject)
        student_exam_score.exam_score += instance.student_score
        student_exam_score.save()

@receiver(post_save, sender=Profile)
def create_student_profile_when_user_role_is_set_to_student(sender, instance, created, **kwargs):
    if created and instance.role == "Student":
        StudentProfile.objects.create(student=instance, admission_date=None)
