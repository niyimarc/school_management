from django.contrib import admin
from .models import (
    ParentProfile, 
    StudentProfile, 
    TeacherProfile, 
    ContinuousAssesment, 
    StudentContinuousAssesmentScore,
    Assignment,
    StudentAssignmentScore,
    Examination,
    StudentExaminationScore,
    StudentTotalGrade,
    StudentCurrentClass,
    )
# Register your models here.
class StudentCurrentClassAdmin(admin.ModelAdmin):
    list_display = ('class_room', 'created_on', 'updated_on')

class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ('parent', 'created_on', 'updated_on')

class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('student', 'admission_date', 'created_on', 'updated_on')

class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'employed_date', 'created_on', 'updated_on')

class ContinuousAssesmentAdmin(admin.ModelAdmin):
    list_display = ('ca_type', 'subject', 'maximum_score', 'description', 'created_on', 'updated_on')

class StudentContinuousAssesmentScoreAdmin(admin.ModelAdmin):
    list_display = ('student', 'ca', 'student_score', 'obtainable_score', 'created_on', 'updated_on')
    readonly_fields = ('obtainable_score',)

class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('subject', 'maximum_score', 'description', 'created_on', 'updated_on')

class StudentAssignmentScoreAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'student_score', 'obtainable_score', 'created_on', 'updated_on')
    readonly_fields = ('obtainable_score',)

class ExaminationAdmin(admin.ModelAdmin):
    list_display = ('subject', 'maximum_score', 'exam_date', 'created_on', 'updated_on')

class StudentExaminationScoreAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'student_score', 'obtainable_score', 'created_on', 'updated_on')
    readonly_fields = ('obtainable_score',)
class StudentTotalGradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'ca_score', 'exam_score', 'total_score', 'student_grade', 'created_on', 'updated_on')

admin.site.register(StudentCurrentClass, StudentCurrentClassAdmin)
admin.site.register(ParentProfile, ParentProfileAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(TeacherProfile, TeacherProfileAdmin)
admin.site.register(ContinuousAssesment, ContinuousAssesmentAdmin)
admin.site.register(StudentContinuousAssesmentScore, StudentContinuousAssesmentScoreAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(StudentAssignmentScore, StudentAssignmentScoreAdmin)
admin.site.register(Examination, ExaminationAdmin)
admin.site.register(StudentExaminationScore, StudentExaminationScoreAdmin)
admin.site.register(StudentTotalGrade, StudentTotalGradeAdmin)