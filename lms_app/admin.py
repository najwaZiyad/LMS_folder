from django.contrib import admin

from .models import *


# Register your models here.


class UsernameSearch(admin.ModelAdmin):
    search_fields = ('last', 'type')
    list_display = ('last', 'type')


class ProfileSearch(admin.ModelAdmin):
    search_fields = ['user__username']
    list_display = ('user', 'first_name', 'role')
    list_filter = ['role']


class SubjectSearch(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'description', 'id')


class TeacherSearch(admin.ModelAdmin):
    search_fields = ('profile__first_name', 'teacher_id')
    list_display = ('profile', 'teacher_id', 'subject')


class StudentSearch(admin.ModelAdmin):
    search_fields = ('profile__first_name', 'student_id')
    list_display = ('profile', 'student_id')


class AttendanceSearch(admin.ModelAdmin):
    search_fields = ('date', 'student_id', 'student', 'teacher', 'teacher_id')
    list_display = ('date', 'time', 'subject', 'student', 'teacher', 'marked_on', 'status')
    list_filter = ['time']


class AssignSearch(admin.ModelAdmin):
    list_display = ('teacher', 'subject')


class TeacherTimeTabelSearch(admin.ModelAdmin):
    list_display = ['teacher', 'subject', 'day', 'time']


class ClassesSearch(admin.ModelAdmin):
    list_display = ['date', 'time', 'cls', 'zoom_link']


class QuizSearch(admin.ModelAdmin):
    list_display = ['created_date', 'start_date', 'end_date', 'subject']


class QuizQuestionSearch(admin.ModelAdmin):
    list_display = ['question', 'answer', 'option_1', 'option_2', 'option_3', 'option_4', 'score']


class QuizStudentSearch(admin.ModelAdmin):
    list_display = ['student', 'subject', 'total_score', 'obtain_score']


class QuizAnswersSearch(admin.ModelAdmin):
    list_display = ['question_id', 'quiz_student', 'answer', 'correct']


class FrontEndDataSearch(admin.ModelAdmin):
    list_display = ['id', 'img', 'num1', 'num2', 'num3', 'num4']


admin.site.register(AutoUsername, UsernameSearch)
admin.site.register(Profile, ProfileSearch)
admin.site.register(Subjects, SubjectSearch)
admin.site.register(Teacher, TeacherSearch)
admin.site.register(TeacherSubjectAssign, AssignSearch)
admin.site.register(TimeTabel, TeacherTimeTabelSearch)
admin.site.register(Classes, ClassesSearch)
admin.site.register(Student, StudentSearch)
admin.site.register(Attendance, AttendanceSearch)
admin.site.register(Quiz, QuizSearch)
admin.site.register(QuizQuestion, QuizQuestionSearch)
admin.site.register(QuizStudent, QuizStudentSearch)
admin.site.register(QuizAnswers, QuizAnswersSearch)
admin.site.register(FrontEndData, FrontEndDataSearch)
admin.site.register(Testimonials)
