import json
import calendar
from datetime import datetime, date, timedelta

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
            teacher = Teacher.objects.create(
                profile=profile, teacher_id=profile.user.username, experience=experience,
                subject=subjects
            )
            for i in subjects:
                TeacherSubjectAssign.objects.create(
                    teacher=teacher, subject=Subjects.objects.get(id=i)
                )
        else:
            last = AutoUsername.objects.get(type='Student')
            Student.objects.create(
                profile=profile, student_id=profile.user.username
            )
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
    messages.success(request, 'Subject ' + name + ' deleted Successfully!')
    return redirect('/view-subjects')


def DeleteUser(request, user_id):
    user = Profile.objects.get(id=user_id)
    name = user.first_name
    user.delete()
    messages.success(request, 'user ' + name + ' deleted Successfully!')
    return redirect('/view-user')


def DeleteTeacherSubjectAssign(request, TeacherSubjectAssign_id):
    teacher = TeacherSubjectAssign.objects.get(id=TeacherSubjectAssign_id)
    name = teacher.teacher.profile.first_name
    teacher.delete()
    messages.success(request, 'teacher ' + str(name) + ' deleted Successfully!')
    return redirect('/view-TeacherSubjectAssign')


def AddSubjects(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        Subjects.objects.create(
            name=name, description=description
        )
        messages.info(request, 'Subject ' + name + ' added Successfully!')
        return redirect('/add-subjects')
    else:
        return render(request, 'dashboard/add_subject.html')


def AddTimeTable(request):
    if request.method == 'POST':
        day = request.POST['day']

        subject_1 = request.POST['subject_1']
        teacher_1 = request.POST.get('teacher_1')
        if subject_1 == 'Free':
            pass
        else:
            subject_1 = Subjects.objects.get(id=subject_1)
            teacher_1 = Teacher.objects.get(id=teacher_1)
            assign1 = TimeTabel.objects.get(day=day, time='7:00 - 7:30')
            assign1.subject = subject_1
            assign1.teacher = teacher_1
            assign1.save()
        subject_2 = request.POST['subject_2']
        teacher_2 = request.POST.get('teacher_2')
        if subject_2 == 'Free':
            pass
        else:
            subject_2 = Subjects.objects.get(id=subject_2)
            teacher_2 = Teacher.objects.get(id=teacher_2)
            assign2 = TimeTabel.objects.get(day=day, time='7:30 - 8:05')
            assign2.subject = subject_2
            assign2.teacher = teacher_2
            assign2.save()
        subject_3 = request.POST['subject_3']
        teacher_3 = request.POST.get('teacher_3')
        if subject_3 == 'Free':
            pass
        else:
            subject_3 = Subjects.objects.get(id=subject_3)
            teacher_3 = Teacher.objects.get(id=teacher_3)
            assign3 = TimeTabel.objects.get(day=day, time='8:05 - 8:45')
            assign3.subject = subject_3
            assign3.teacher = teacher_3
            assign3.save()
        subject_4 = request.POST['subject_4']
        teacher_4 = request.POST.get('teacher_4')
        if subject_4 == 'Free':
            pass
        else:
            subject_4 = Subjects.objects.get(id=subject_4)
            teacher_4 = Teacher.objects.get(id=teacher_4)
            assign4 = TimeTabel.objects.get(day=day, time='8:45 - 9:00')
            assign4.subject = subject_4
            assign4.teacher = teacher_4
            assign4.save()
        subject_5 = request.POST['subject_5']
        teacher_5 = request.POST.get('teacher_5')
        if subject_5 == 'Free':
            pass
        else:
            subject_5 = Subjects.objects.get(id=subject_5)
            teacher_5 = Teacher.objects.get(id=teacher_5)
            assign5 = TimeTabel.objects.get(day=day, time='9:00 - 9:15')
            assign5.subject = subject_5
            assign5.teacher = teacher_5
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
        current = TimeTabel.objects.get(day=day, time='9:00 - 9:15')
        # current_timetable = []
        # for i in current:
        #     current_timetable.append(i)
        data = {'days': days, 'subjects': subjects, 'time': time, 'day': day, 'current': current}
        return render(request, 'dashboard/add_time_table.html', data)
    else:
        return redirect('/add-subjects')


def addClass(request):
    if request.method == 'POST':
        added_on = datetime.now()
        my_date = request.POST['date']
        time_id = request.POST['time']
        zoom_link = request.POST['link']
        time = TimeTabel.objects.get(id=time_id)
        cls = time.subject
        time = time.time
        try:
            Classes.objects.get(date=my_date, time=time)
            messages.info(request, 'Zoom Link was already assigned on selected date and time!')
        except Classes.DoesNotExist:
            Classes.objects.create(
                added_on=added_on, date=my_date, zoom_link=zoom_link, time=time, cls=cls, added_by=request.user.profile
            )
            Classes.objects.filter(date__lt=(date.today() - timedelta(days=2))).delete()
            messages.info(request, 'Zoom Link Added Successfully!')
        return redirect('/view-class')
    else:
        today = date.today()
        last_date = date.today() + timedelta(days=1)
        data = {'today': str(today), 'last_date': str(last_date)}
        return render(request, 'dashboard/teacher/classes.html', data)


def editLinks(request, id):
    if request.method == 'POST':
        my_date = request.POST['date']
        time_id = request.POST['time']
        zoom_link = request.POST['link']
        time = TimeTabel.objects.get(id=time_id)
        cls = time.subject
        time = time.time

        e = Subjects.objects.get(id=id)
        e.date = my_date
        e.time = time_id
        e.link = zoom_link
        e.save()
        messages.info(request, 'data  updated successfully!')
        return redirect('/view-class')

    else:
        links = Classes.objects.get(id=id)
        data = {'links': links}
        return render(request, '/view-class', data)


def viewClass(request):
    if request.method == 'POST':
        pass
    else:
        links = Classes.objects.filter(added_by=request.user.profile)
        data = {'links': links}
        return render(request, 'dashboard/teacher/view_classes.html', data)


def DeleteClassLink(request, i_id):
    classs = Classes.objects.get(id=i_id)
    date = classs.date
    classs.delete()
    messages.success(request, 'classs ' + str(date) + ' deleted Successfully!')
    return redirect('/view-class')


def selectSubject(request):
    profile = request.user.profile
    if request.method == "POST":
        subject_id = request.POST['id']
        my_date = request.POST['date']
        time = request.POST['time']
        time = TimeTabel.objects.get(id=time).time
        students_query = Student.objects.all()
        students = []
        n = 0
        for i in students_query:
            n += 1
            students.append({'student': i, 'n': n})
        attendance = Attendance.objects.filter(date=my_date, time=time)
        att_list = []
        if attendance:
            n = 'num_'
            m = 0
            for i in Student.objects.all():
                m += 1
                dic = {}
                att = Attendance.objects.filter(date=my_date, time=time, student_id=i.student_id).first()
                if att:
                    dic['student'] = i.profile.first_name
                    dic['student_id'] = i.student_id
                    dic['id'] = att.id
                    dic['status'] = att.status
                else:
                    dic['student'] = i.profile.first_name
                    dic['student_id'] = i.student_id
                    dic['id'] = n + str(m)
                    dic['status'] = 'Unmarked'
                att_list.append(dic)
            n = 0

        data = {'date': my_date, 'subject_id': subject_id, 'time': time, 'students': students,
                'n': n, 'attendance': att_list}
        return render(request, 'dashboard/teacher/mark_attendance.html', data)
    else:
        subjects = TeacherSubjectAssign.objects.filter(teacher=profile.teacher)
        data = {'subjects': subjects}
        return render(request, 'dashboard/teacher/select_class.html', data)


def markAttendance(request):
    profile = request.user.profile
    if request.method == "POST":
        subject_id = request.POST['subject_id']
        subject = Subjects.objects.get(id=int(subject_id))
        my_date = request.POST['date']
        time = request.POST['time']
        student_id = request.POST['student_id']
        student = Student.objects.get(student_id=student_id)
        status = request.POST['status']
        try:
            att = Attendance.objects.get(date=my_date, time=time, student_id=student.student_id)
            att.status = status
            att.marked_on = datetime.now()
            att.save()
        except Attendance.DoesNotExist:
            Attendance.objects.create(
                subject=subject.name, subject_id=subject.id, date=my_date, time=time,
                student=student.profile, student_id=student.student_id, teacher=profile,
                teacher_id=profile.teacher.teacher_id, status=status, marked_on=datetime.now()
            )
        return HttpResponse('Success')


def getClasses(request):
    profile = request.user.profile.teacher
    subject_id = request.POST['id']
    my_date = request.POST['date']
    my_date = datetime.strptime(my_date, '%Y-%m-%d')
    day = calendar.day_name[my_date.weekday()]
    subject = Subjects.objects.get(id=subject_id)
    time_table = TimeTabel.objects.filter(teacher=profile, day=day, subject=subject)
    time = []
    for i in time_table:
        time.append({'id': i.id, 'time': str(i.time), 'subject': str(i.subject)})
    return HttpResponse(json.dumps(time))


def getSubject(request):
    id = request.POST['id']
    subject = Subjects.objects.get(id=id)
    teachers = TeacherSubjectAssign.objects.filter(subject=subject)
    teacher = []
    for i in teachers:
        dic = {}
        dic['id'] = i.teacher.id
        dic['name'] = i.teacher.profile.first_name + " " + i.teacher.profile.second_name + " " + i.teacher.profile.third_name + " " + i.teacher.profile.last_name
        teacher.append(dic)
    return HttpResponse(json.dumps(teacher))


def getTeacherSubject(request):
    day_date = request.POST['date']
    day_date = datetime.strptime(day_date, '%Y-%m-%d').weekday()
    day = calendar.day_name[day_date]
    time_table = TimeTabel.objects.filter(day=day, teacher=request.user.profile.teacher)
    time = []
    for i in time_table:
        time.append({'id': i.id, 'time': str(i.time), 'subject': str(i.subject)})
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


def createTimetable(request):
    for i in DAYS_OF_WEEK:
        for j in time_slots:
            try:
                TimeTabel.objects.get(day=i[0], time=j[0])
            except TimeTabel.DoesNotExist:
                TimeTabel.objects.create(
                    day=i[0], time=j[0]
                )
