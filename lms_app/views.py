import json
import calendar
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout

def IndexPage(request):
    return render(request, 'front/index.html')


def LogoutFun(request):
    logout(request)
    return redirect('/login')

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/dashboard")
        else:
            messages.error(request, 'Invalid user !')
            return redirect("/login")
    else:
        return render(request, 'dashboard/login.html')

def DashboardRedirect(request):
    role = request.user.profile.role
    if role == 'student':
        return redirect('/student-dashboard')
    elif role == 'teacher':
        return redirect('/teacher-dashboard')
    else:
        return redirect('/admin-dashboard')




def AdminDashboard(request):
    time = []
    for i in time_slots:
        time.append(i[0])
    saturday = TimeTabel.objects.filter(day='Saturday').order_by('time')
    sunday = TimeTabel.objects.filter(day='Sunday').order_by('time')
    monday = TimeTabel.objects.filter(day='Monday').order_by('time')
    tuesday = TimeTabel.objects.filter(day='Tuesday').order_by('time')
    wednesday = TimeTabel.objects.filter(day='Wednesday').order_by('time')
    thursday = TimeTabel.objects.filter(day='Thursday').order_by('time')
    friday = TimeTabel.objects.filter(day='Friday').order_by('time')
    data = {'saturday': saturday, 'sunday': sunday, 'time': time, 'monday': monday, 'tuesday': tuesday,
            'wednesday': wednesday, 'thursday': thursday, 'friday': friday}
    return render(request, 'dashboard/admin_dashboard.html', data)


def StudentDashboard(request):
    time = []
    for i in time_slots:
        time.append(i[0])
    saturday = TimeTabel.objects.filter(day='Saturday').order_by('time')
    sunday = TimeTabel.objects.filter(day='Sunday').order_by('time')
    monday = TimeTabel.objects.filter(day='Monday').order_by('time')
    tuesday = TimeTabel.objects.filter(day='Tuesday').order_by('time')
    wednesday = TimeTabel.objects.filter(day='Wednesday').order_by('time')
    thursday = TimeTabel.objects.filter(day='Thursday').order_by('time')
    friday = TimeTabel.objects.filter(day='Friday').order_by('time')
    data = {'saturday': saturday, 'sunday': sunday, 'time': time, 'monday': monday, 'tuesday': tuesday,
            'wednesday': wednesday, 'thursday': thursday, 'friday': friday}
    return render(request, 'dashboard/student/dashboard.html', data)

def TeacherDashboard(request):
    time = []
    for i in time_slots:
        time.append(i[0])
    saturday = TimeTabel.objects.filter(day='Saturday').order_by('time')
    sunday = TimeTabel.objects.filter(day='Sunday').order_by('time')
    monday = TimeTabel.objects.filter(day='Monday').order_by('time')
    tuesday = TimeTabel.objects.filter(day='Tuesday').order_by('time')
    wednesday = TimeTabel.objects.filter(day='Wednesday').order_by('time')
    thursday = TimeTabel.objects.filter(day='Thursday').order_by('time')
    friday = TimeTabel.objects.filter(day='Friday').order_by('time')
    data = {'saturday': saturday, 'sunday': sunday, 'time': time, 'monday': monday, 'tuesday': tuesday,
            'wednesday': wednesday, 'thursday': thursday, 'friday': friday}
    return render(request, 'dashboard/teacher/dashboard.html', data)

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


def viewUser(request):
    data = {'profiles': Profile.objects.all()}
    return render(request, 'dashboard/view_users.html', data)

def editUser(request, id):
    if request.method == 'POST':
        password = request.POST['password']
        f = request.POST['name1']
        s = request.POST['name2']
        t = request.POST['name3']
        l = request.POST['name4']
        add = request.POST['address']
        e = Profile.objects.get(id=id)
        e.first_name = f
        e.second_name = s
        e.third_name = t
        e.last_name = l
        e.address = add
        e.save()
        if password:
            user = User.objects.get(user=e.user)
            user.password = make_password(password)
            user.save()
        messages.info(request, 'User information changed successfully!')
        return redirect('/view-user')
    else:
        profile = Profile.objects.get(id=id)
        data = {'profile': profile}
        return render(request, 'dashboard/edit_user.html', data)

def ViewSubjects(request):
    data = {'subjects': Subjects.objects.all()}
    return render(request, 'dashboard/view_subjects.html', data)


def editSubjects(request, id):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']

        e = Subjects.objects.get(id=id)
        e.name = name
        e.description = description
        e.save()
        messages.info(request, 'subject information updated successfully!')
        return redirect('/view-subjects')

    else:
        subject = Subjects.objects.get(id=id)
        data = {'subject': subject}
        return render(request, 'dashboard/edit_subject.html', data)


def DeleteSubjects(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    name = subject.name
    subject.delete()
    messages.success(request, 'Subject '+name+' deleted Successfully!')
    return redirect('/view-subjects')


def DeleteUser(request, user_id):
    user = Profile.objects.get(id=user_id)
    name = user.first_name
    user.delete()
    messages.success(request, 'user '+name+' deleted Successfully!')
    return redirect('/view-user')


def DeleteTeacherSubjectAssign(request, TeacherSubjectAssign_id):
    teacher = TeacherSubjectAssign.objects.get(id=TeacherSubjectAssign_id)
    name = teacher.teacher.profile.first_name
    teacher.delete()
    messages.success(request, 'teacher '+str(name)+' deleted Successfully!')
    return redirect('/view-TeacherSubjectAssign')

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
        subject_1 = request.POST['subject_1']
        subject_1 = Subjects.objects.get(id=subject_1)
        subject_2 = request.POST['subject_2']
        subject_2 = Subjects.objects.get(id=subject_2)
        subject_3 = request.POST['subject_3']
        subject_3 = Subjects.objects.get(id=subject_3)
        subject_4 = request.POST['subject_4']
        subject_4 = Subjects.objects.get(id=subject_4)
        subject_5 = request.POST['subject_5']
        subject_5 = Subjects.objects.get(id=subject_5)
        teacher_1 = request.POST['teacher_1']
        teacher_1 = Teacher.objects.get(id=teacher_1)
        teacher_2 = request.POST['teacher_2']
        teacher_2 = Teacher.objects.get(id=teacher_2)
        teacher_3 = request.POST['teacher_3']
        teacher_3 = Teacher.objects.get(id=teacher_3)
        teacher_4 = request.POST['teacher_4']
        teacher_4 = Teacher.objects.get(id=teacher_4)
        teacher_5 = request.POST['teacher_5']
        teacher_5 = Teacher.objects.get(id=teacher_5)
        day = request.POST['day']

        assign1 = TimeTabel.objects.get(day=day, time='7:00 - 7:30')
        assign2 = TimeTabel.objects.get(day=day, time='7:30 - 8:05')
        assign3 = TimeTabel.objects.get(day=day, time='8:05 - 8:45')
        assign4 = TimeTabel.objects.get(day=day, time='8:45 - 9:00')
        assign5 = TimeTabel.objects.get(day=day, time='9:00 - 9:15')
        assign1.subject = subject_1
        assign2.subject = subject_2
        assign3.subject = subject_3
        assign4.subject = subject_4
        assign5.subject = subject_5

        assign1.teacher = teacher_1
        assign2.teacher = teacher_2
        assign3.teacher = teacher_3
        assign4.teacher = teacher_4
        assign5.teacher = teacher_5
        assign1.save()
        assign2.save()
        assign3.save()
        assign4.save()
        assign5.save()
        return redirect('/admin-dashboard')
    else:
        pass

def AssignTimeTable(request):
    if request.method == 'POST':
        subjects = Subjects.objects.all()
        days = []
        for i in DAYS_OF_WEEK:
            days.append(i[0])
        time = []
        n = 0
        for i in time_slots:
            n += 1
            time.append({'n': n, 'time': i[0]})
        day = request.POST['day']
        data = {'days': days, 'subjects': subjects, 'time': time, 'day': day}
        return render(request, 'dashboard/add_time_table.html', data)
    else:
        return redirect('/add-subjects')

def addClass(request):
    return render(request, 'dashboard/teacher/classes.html')

def getSubject(request):
    id = request.POST['id']
    subject = Subjects.objects.get(id=id)
    teachers = TeacherSubjectAssign.objects.filter(subject=subject)
    teacher = []
    for i in teachers:
        dic = {}
        dic['id'] = i.teacher.id
        dic['name'] = i.teacher.profile.first_name +" "+ i.teacher.profile.second_name +" "+ i.teacher.profile.third_name +" "+ i.teacher.profile.last_name
        teacher.append(dic)
    return HttpResponse(json.dumps(teacher))


def getTeacherSubject(request):
    day_date = request.POST['date']
    day_date = datetime.strptime(day_date, '%Y-%m-%d').weekday()
    day = calendar.day_name[day_date]
    time_table = TimeTabel.objects.filter(day=day, teacher=request.user.profile.teacher)
    time = []
    for i in time_table:
        time.append(i.time)
    return HttpResponse(json.dumps(time))



def ViewTeacherSubjectAssign(request):
    if request.method == "POST":
        teacher_id = request.POST['teachers']
        teacher = Teacher.objects.get(id=teacher_id)
        subjects = request.POST.getlist('subject')
        for s in subjects:
            subject = Subjects.objects.get(id=s)
            try:
                TeacherSubjectAssign.objects.get(teacher=teacher, subject=subject)
            except TeacherSubjectAssign.DoesNotExist:
                TeacherSubjectAssign.objects.create(
                    teacher=teacher, subject=subject
                )
        messages.info(request, 'Successfully Added')
        return redirect('/view-TeacherSubjectAssign')
    else:
        assignment = TeacherSubjectAssign.objects.all()
        najwa = Subjects.objects.all()
        teachers = Teacher.objects.all()
        data = {'assignments': assignment, 'subjects': najwa, 'teachers': teachers}
        return render(request, 'dashboard/TeacherSubjectAssign.html', data)
