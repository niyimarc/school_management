from django.contrib import admin
from .models import SchoolSession, SchoolHoliday, Subject, ClassRoom
# Register your models here.

class SchoolSessionAdmin(admin.ModelAdmin):
    list_display = ('session_term', 'session_year', 'start_date', 'end_date', 'number_of_time_school_opened', 'created_on', 'updated_on')

class SchoolHolidayAdmin(admin.ModelAdmin):
    list_display = ('session', 'about', 'start_date', 'resumption_date', 'created_on', 'updated_on')

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_name', 'subject_teacher', 'class_room', 'subject_description', 'created_on', 'updated_on')

class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ('class_room_name', 'class_arm', 'class_administrator', 'session', 'created_on', 'updated_on')



admin.site.register(SchoolSession, SchoolSessionAdmin)
admin.site.register(SchoolHoliday, SchoolHolidayAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(ClassRoom, ClassRoomAdmin)
