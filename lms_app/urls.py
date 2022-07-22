from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexPage),
    path('login', LoginPage),
    path('admin-dashboard', AdminDashboard),
    path('add-user', AddUser),
    path('view-user', viewUser),
    path('edit-user/<int:id>', editUser),
    path('add-subjects', AddSubjects),
    path('view-subjects', ViewSubjects),
    path('edit-subject/<int:id>', editSubjects),
    path('delete-subjects/<int:subject_id>', DeleteSubjects),

    path('delete-user/<int:user_id>', DeleteUser),
    path('delete-TeacherSubjectAssign/<int:TeacherSubjectAssign_id>', DeleteTeacherSubjectAssign),

    path('view-TeacherSubjectAssign', ViewTeacherSubjectAssign),
    path('add-time-table', AddTimeTable),
    path('get-subject', getSubject),
]
