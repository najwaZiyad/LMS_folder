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
    search_fields = ('name', 'teacher_id')
    list_display = ('name', 'description', 'teacher_id')


class TeacherSearch(admin.ModelAdmin):
    search_fields = ('profile', 'teacher_id')
    list_display = ('profile', 'teacher_id', 'subjects')


admin.site.register(AutoUsername, UsernameSearch)
admin.site.register(Profile, ProfileSearch)
admin.site.register(Subjects, SubjectSearch)
admin.site.register(Teacher, TeacherSearch)