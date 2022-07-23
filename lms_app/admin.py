from django.contrib import admin
from .models import *

# Register your models here.


class UsernameSearch(admin.ModelAdmin):
    search_fields = ('last', 'type')
    list_display = ('last', 'type')

class ProfileSearch(admin.ModelAdmin):
    search_fields = ['user__username']
    list_display = ('user', 'first_name','role')
    list_filter = ['role']


class SubjectSearch(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', 'description', )


class TeacherSearch(admin.ModelAdmin):
    search_fields = ('profile', 'teacher_id')
    list_display = ('profile', 'teacher_id', 'subject')

class AssignSearch(admin.ModelAdmin):
    list_display = ('teacher', 'subject')

class TeacherTimeTabelSearch(admin.ModelAdmin):
    list_display = ['teacher', 'subject', 'day', 'time']

class ClassesSearch(admin.ModelAdmin):
    list_display = ['date', 'time', 'cls', 'zoom_link']

admin.site.register(AutoUsername, UsernameSearch)
admin.site.register(Profile, ProfileSearch)
admin.site.register(Subjects, SubjectSearch)
admin.site.register(Teacher, TeacherSearch)
admin.site.register(TeacherSubjectAssign, AssignSearch)
admin.site.register(TimeTabel, TeacherTimeTabelSearch)
admin.site.register(Classes, ClassesSearch)
