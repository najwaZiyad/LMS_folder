import json

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout

def IndexPage(request):
    return render(request, 'front/index.html')

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/admin-dashboard")
        else:
            messages.error(request, 'Invalid user !')
            return redirect("/login")
    else:
        return render(request, 'dashboard/login.html')


def AdminDashboard(request):
    teacher = AutoUsername.objects.get(type='Teacher').last
    student = AutoUsername.objects.get(type='Student').last
    data = {'teacher': teacher, 'student': student}
    return render(request, 'dashboard/admin_dashboard.html', data)


def AddUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        role = request.POST['role']
        name1 = request.POST['name1']
        name2 = request.POST.get('name2')
        name3 = request.POST.get('name3')
        name4 = request.POST.get('name4')
        address = request.POST['address']
        profile = Profile.objects.create(user=user, first_name=name1, second_name=name2, third_name=name3,
                                         last_name=name4, address=address, role=role)
        if role == 'teacher':
            last = AutoUsername.objects.get(type='Teacher')
            experience = request.POST['experience']
            subjects = request.POST.getlist('subject')
            teacher= Teacher.objects.create(
                profile=profile, teacher_id=profile.user.username, experience=experience,
                subject=subjects
            )
            for i in subjects:
                TeacherSubjectAssign.objects.create(
                    teacher=teacher, subject=Subjects.objects.get(id=i)
                )
        else:
            last = AutoUsername.objects.get(type='Student')
        last.last = int(last.last) + 1
        last.save()
        return redirect('/add-user')
    else:
        teacher = AutoUsername.objects.get(type='Teacher').last
        student = AutoUsername.objects.get(type='Student').last
        subjects = Subjects.objects.all()
        data = {'teacher': teacher, 'student': student, 'subjects': subjects}
        return render(request, 'dashboard/add_user.html', data)


def AddSubjects(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        Subjects.objects.create(
            name=name, description=description
        )
        messages.info(request, 'Subject '+name+' added Successfully!')
        return redirect('/add-subjects')
    else:
        return render(request, 'dashboard/add_subject.html')

def AddTimeTable(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        Subjects.objects.create(
            name=name, description=description
        )
        messages.info(request, 'Subject '+name+' added Successfully!')
        return redirect('/add-subjects')
    else:
        subjects = Subjects.objects.all()
        days = []
        for i in DAYS_OF_WEEK:
            days.append(i[0])
        time = []
        for i in time_slots:
            time.append(i[0])
        data = {'days': days, 'subjects': subjects, 'time': time}
        return render(request, 'dashboard/add_time_table.html', data)

def getSubject(request):
    id = request.POST['id']
    subject = Subjects.objects.get(id=id)
    teachers = TeacherSubjectAssign.objects.filter(subject=subject)
    teacher = []
    for i in teachers:
        dic = {}
        dic['id'] = i.teacher.id
        dic['name'] = i.teacher.profile.first_name
        teacher.append(dic)
    return HttpResponse(json.dumps(teacher))


