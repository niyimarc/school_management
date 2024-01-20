from django.contrib import admin
from .models import ParentProfile, StudentProfile, TeacherProfile
# Register your models here.

class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ('parent', 'created_on', 'updated_on')

class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('student', 'admission_date', 'current_class', 'created_on', 'updated_on')

class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'employed_date', 'created_on', 'updated_on')


admin.site.register(ParentProfile, ParentProfileAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(TeacherProfile, TeacherProfileAdmin)