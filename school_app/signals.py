from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StudentContinuousAssesmentScore, StudentTotalGrade

@receiver(post_save, sender=StudentContinuousAssesmentScore)
def update_student_ca_score(sender, instance, created, **kwargs):
    if created:
        student_ca_score, created = StudentTotalGrade.objects.get_or_create(student=instance.student, subject=instance.ca.subject)
        student_ca_score.ca_score += instance.student_score
        student_ca_score.save()