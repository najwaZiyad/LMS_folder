from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexPage),
    path('login', LoginPage),
    path('logout', LogoutFun),

    path('dashboard', DashboardRedirect),
    path('admin-dashboard', AdminDashboard),
    path('student-dashboard', StudentDashboard),
    path('teacher-dashboard', TeacherDashboard),

    path('add-user', AddUser),
    path('view-user', viewUser),
    path('edit-user/<int:id>', editUser),
    path('add-subjects', AddSubjects),
    path('view-subjects', ViewSubjects),
    path('edit-subject/<int:id>', editSubjects),

    path('edit-timetable', AssignTimeTable),
    path('add-time-table', AddTimeTable),

    path('delete-user/<int:user_id>', DeleteUser),
    path('delete-TeacherSubjectAssign/<int:TeacherSubjectAssign_id>', DeleteTeacherSubjectAssign),

    path('view-TeacherSubjectAssign', ViewTeacherSubjectAssign),


    # Teacher
    path('add-class', addClass),
    path('view-class', viewClass),
    path('delete-classLink/<int:i_id>', DeleteClassLink),
    path('select-subject', selectSubject),
    path('mark-attendance', markAttendance),

    # Student
    path('attendance-subject', attendanceSubject),
    path('classes', studentClasses),

    path('get-subject', getSubject),
    path('get-teacher-subject', getTeacherSubject),
    path('get-classes', getClasses),
    path('settings', Settings),
    path('change-password', change_password),
    path('upload-image', uploadImage),

    path('create-empty-timetable', createTimetable),
]
