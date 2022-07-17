from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexPage),
    path('login', LoginPage),
    path('admin-dashboard', AdminDashboard),
    path('add-user', AddUser),
    path('add-subjects', AddSubjects),
    path('add-time-table', AddTimeTable),
    path('get-subject', getSubject),
]
