import calendar
import csv
import json
from datetime import datetime, date, timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage

from .models import *


def view_404(request, exception=None):
    return render(request, '404.html')


def IndexPage(request):
    f = FrontEndData.objects.first()
    testimonials = Testimonials.objects.all()
    data = {'f': f, 'testimonials': testimonials}
    return render(request, 'front/index.html', data)


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
        if request.user.is_authenticated:
            return redirect('/dashboard')
        else:
            return render(request, 'dashboard/login.html')


@login_required
def DashboardRedirect(request):
    role = request.user.profile.role
    if role == 'student':
        return redirect('/student-dashboard')
    elif role == 'teacher':
        return redirect('/teacher-dashboard')
    elif role == 'admin':
        return redirect('/admin-dashboard')
    else:
        messages.error(request, 'Something Went Wrong Contact Admin!')
        return redirect('/logout')


@login_required
def AdminDashboard(request):
    role = request.user.profile.role
    if role == 'admin':
        old_time = []
        for i in time_slots:
            old_time.append(i[0])
        time = []
        a = 0
        n = len(old_time) - 1
        while a < len(old_time):
            a += 1
            time.append(old_time[n])
            n -= 1

        saturday = TimeTabel.objects.filter(day='Saturday').order_by('-time')
        sunday = TimeTabel.objects.filter(day='Sunday').order_by('-time')
        monday = TimeTabel.objects.filter(day='Monday').order_by('-time')
        tuesday = TimeTabel.objects.filter(day='Tuesday').order_by('-time')
        wednesday = TimeTabel.objects.filter(day='Wednesday').order_by('-time')
        thursday = TimeTabel.objects.filter(day='Thursday').order_by('-time')
        friday = TimeTabel.objects.filter(day='Friday').order_by('-time')
        data = {'saturday': saturday, 'sunday': sunday, 'time': time, 'monday': monday, 'tuesday': tuesday,
                'wednesday': wednesday, 'thursday': thursday, 'friday': friday}
        return render(request, 'dashboard/admin_dashboard.html', data)
    else:
        messages.warning(request, 'Unauthorized Access!')
        return redirect('/dashboard')


@login_required
def StudentDashboard(request):
    role = request.user.profile.role
    if role == 'student':
        old_time = []
        for i in time_slots:
            old_time.append(i[0])
        time = []
        a = 0
        n = len(old_time) - 1
        while a < len(old_time):
            a += 1
            time.append(old_time[n])
            n -= 1
        saturday = TimeTabel.objects.filter(day='Saturday').order_by('-time')
        sunday = TimeTabel.objects.filter(day='Sunday').order_by('-time')
        monday = TimeTabel.objects.filter(day='Monday').order_by('-time')
        tuesday = TimeTabel.objects.filter(day='Tuesday').order_by('-time')
        wednesday = TimeTabel.objects.filter(day='Wednesday').order_by('-time')
        thursday = TimeTabel.objects.filter(day='Thursday').order_by('-time')
        friday = TimeTabel.objects.filter(day='Friday').order_by('-time')
        data = {'saturday': saturday, 'sunday': sunday, 'time': time, 'monday': monday, 'tuesday': tuesday,
                'wednesday': wednesday, 'thursday': thursday, 'friday': friday}
        return render(request, 'dashboard/student/dashboard.html', data)
    else:
        messages.warning(request, 'Unauthorized Access!')
        return redirect('/dashboard')


@login_required
def TeacherDashboard(request):
    role = request.user.profile.role
    if role == 'teacher':
        old_time = []
        for i in time_slots:
            old_time.append(i[0])
        time = []
        a = 0
        n = len(old_time) - 1
        while a < len(old_time):
            a += 1
            time.append(old_time[n])
            n -= 1
        saturday = TimeTabel.objects.filter(day='Saturday').order_by('-time')
        sunday = TimeTabel.objects.filter(day='Sunday').order_by('-time')
        monday = TimeTabel.objects.filter(day='Monday').order_by('-time')
        tuesday = TimeTabel.objects.filter(day='Tuesday').order_by('-time')
        wednesday = TimeTabel.objects.filter(day='Wednesday').order_by('-time')
        thursday = TimeTabel.objects.filter(day='Thursday').order_by('-time')
        friday = TimeTabel.objects.filter(day='Friday').order_by('-time')
        data = {'saturday': saturday, 'sunday': sunday, 'time': time, 'monday': monday, 'tuesday': tuesday,
                'wednesday': wednesday, 'thursday': thursday, 'friday': friday}
        return render(request, 'dashboard/teacher/dashboard.html', data)
    else:
        messages.warning(request, 'Unauthorized Access!')
        return redirect('/dashboard')


@login_required
def attendanceSubject(request):
    role = request.user.profile.role
    if role == 'student':
        student_id = request.user.profile.student.student_id
        if request.method == 'POST':
            subject_id = request.POST['subject_id']
            att = Attendance.objects.filter(student_id=student_id, subject_id=subject_id)
            data = {'att': att}
            return render(request, 'dashboard/student/class_attendance.html', data)
        else:
            subject_query = Subjects.objects.all()
            subjects = []
            for i in subject_query:
                dic = {}
                dic['subject'] = i
                dic['absent'] = Attendance.objects.filter(subject_id=i.id, student_id=student_id,
                                                          status='Absent').count()
                dic['present'] = Attendance.objects.filter(subject_id=i.id, student_id=student_id,
                                                           status='Present').count()
                dic['total'] = Attendance.objects.filter(subject_id=i.id, student_id=student_id).count()
                if dic['total'] > 0:
                    dic['percentage'] = dic['present'] / dic['total'] * 100
                else:
                    dic['percentage'] = '-'
                subjects.append(dic)
            data = {'subjects': subjects}
            return render(request, 'dashboard/student/attendance_class.html', data)
    else:
        messages.warning(request, 'Unauthorized Access!')
        return redirect('/dashboard')


@login_required
def studentClasses(request):
    role = request.user.profile.role
    if role == 'student':
        links = Classes.objects.filter(date=date.today())
        data = {'links': links}
        return render(request, 'dashboard/student/classes.html', data)
    else:
        messages.warning(request, 'Unauthorized Access!')
        return redirect('/dashboard')


@login_required
def Settings(request):
    form = PasswordChangeForm(request.user)
    data = {'form': form}
    return render(request, 'dashboard/settings.html', data)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            logout(request)
            return redirect('/login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'dashboard/settings.html', {'form': form})


@login_required
def uploadImage(request):
    if request.method == 'POST':
        user_image = request.FILES['user-img']
        id = request.POST['id']
        prof = Profile.objects.get(id=id)
        prof.img = user_image
        prof.save()
        return redirect('/dashboard')


@login_required
def AddUser(request):
    role = request.user.profile.role
    if role == 'admin':
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
    else:
        messages.warning(request, 'Unauthorized Access!')
        return redirect('/dashboard')


@login_required
def viewUser(request):
    role = request.user.profile.role
    if role == 'admin':
        data = {'profiles': Profile.objects.all()}
        return render(request, 'dashboard/view_users.html', data)
    else:
        messages.warning(request, 'Unauthorized Access!')
        return redirect('/dashboard')


@login_required
def editUser(request, id):
    role = request.user.profile.role
    if role == 'admin':
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
                user = User.objects.get(username=e.user)
                user.password = make_password(password)
                user.save()
            messages.info(request, 'User information changed successfully!')
            return redirect('/view-user')
        else:
            profile = Profile.objects.get(id=id)
            data = {'profile': profile}
            return render(request, 'dashboard/edit_user.html', data)
    else:
        messages.warning(request, 'Unauthorized Access!')
        return redirect('/dashboard')


@login_required
def delete_user(request, id):
    role = request.user.profile.role
    if role == 'admin':
        Profile.objects.get(id=id).delete()
        messages.info(request, 'User deleted successfully!')
        return redirect('/view-user')
    else:
        messages.warning(request, 'Unauthorized Access!')
        return redirect('/dashboard')


@login_required
def quiz_delete(request, id):
    role = request.user.profile.role
    if role == 'teacher':
        quiz = Quiz.objects.get(id=id)
        if quiz.teacher_id == request.user.profile.teacher.teacher_id:
            quiz.delete()
            messages.info(request, 'Quiz deleted successfully!')
        else:
            messages.info(request, 'You are not the creater and hence cannot be deleted by you.')
        return redirect('/quiz')
    else:
        messages.warning(request, 'Unauthorized Access!')
        return redirect('/dashboard')


@login_required
def delete_subjects(request, id):
    role = request.user.profile.role
    if role == 'admin':
        Subjects.objects.get(id=id).delete()
        messages.info(request, 'Subject deleted successfully!')
        return redirect('/view-subjects')
    else:
        messages.warning(request, 'Unauthorized Access!')
        return redirect('/dashboard')


@login_required
def ViewSubjects(request):
    role = request.user.profile.role
    if role == 'admin':
        data = {'subjects': Subjects.objects.all()}
        return render(request, 'dashboard/view_subjects.html', data)
    else:
        messages.warning(request, 'Unauthorized Access!')
        return redirect('/dashboard')


@login_required
def editSubjects(request, id):
    role = request.user.profile.role
    if role == 'admin':
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
    else:
        messages.warning(request, 'Unauthorized Access!')
        return redirect('/dashboard')


@login_required
def DeleteUser(request, user_id):
    return redirect('/view-user')


@login_required
def DeleteTeacherSubjectAssign(request, TeacherSubjectAssign_id):
    role = request.user.profile.role
    if role == 'admin':
        teacher = TeacherSubjectAssign.objects.get(id=TeacherSubjectAssign_id)
        name = teacher.teacher.profile.first_name
        teacher.delete()
        messages.success(request, 'teacher ' + str(name) + ' deleted Successfully!')
        return redirect('/view-TeacherSubjectAssign')
    else:
        messages.warning(request, 'Unauthorized Access!')
        return redirect('/dashboard')


@login_required
def AddSubjects(request):
    role = request.user.profile.role
    if role == 'admin':
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
    else:
        messages.warning(request, 'Unauthorized Access!')
        return redirect('/dashboard')


@login_required
def AddTimeTable(request):
    role = request.user.profile.role
    if role == 'admin':
        if request.method == 'POST':
            day = request.POST['day']
            subject_1 = request.POST['subject_1']
            teacher_1 = request.POST.get('teacher_1')
            assign1 = TimeTabel.objects.get(day=day, time='7:00 - 7:30')
            if subject_1 == 'Free':
                assign1.subject = None
                assign1.teacher = None
                assign1.save()
            else:
                subject_1 = Subjects.objects.get(id=subject_1)
                teacher_1 = Teacher.objects.get(id=teacher_1)
                assign1.subject = subject_1
                assign1.teacher = teacher_1
                assign1.save()
            subject_2 = request.POST['subject_2']
            teacher_2 = request.POST.get('teacher_2')
            assign2 = TimeTabel.objects.get(day=day, time='7:30 - 8:05')
            if subject_2 == 'Free':
                assign2.subject = None
                assign2.teacher = None
                assign2.save()
            else:
                subject_2 = Subjects.objects.get(id=subject_2)
                teacher_2 = Teacher.objects.get(id=teacher_2)
                assign2.subject = subject_2
                assign2.teacher = teacher_2
                assign2.save()
            subject_3 = request.POST['subject_3']
            teacher_3 = request.POST.get('teacher_3')
            assign3 = TimeTabel.objects.get(day=day, time='8:05 - 8:45')
            if subject_3 == 'Free':
                assign3.subject = None
                assign3.teacher = None
                assign3.save()
            else:
                subject_3 = Subjects.objects.get(id=subject_3)
                teacher_3 = Teacher.objects.get(id=teacher_3)
                assign3.subject = subject_3
                assign3.teacher = teacher_3
                assign3.save()
            subject_4 = request.POST['subject_4']
            teacher_4 = request.POST.get('teacher_4')
            assign4 = TimeTabel.objects.get(day=day, time='8:45 - 9:00')
            if subject_4 == 'Free':
                assign4.subject = None
                assign4.teacher = None
                assign4.save()
            else:
                subject_4 = Subjects.objects.get(id=subject_4)
                teacher_4 = Teacher.objects.get(id=teacher_4)
                assign4.subject = subject_4
                assign4.teacher = teacher_4
                assign4.save()
            subject_5 = request.POST['subject_5']
            teacher_5 = request.POST.get('teacher_5')
            assign5 = TimeTabel.objects.get(day=day, time='9:00 - 9:15')
            if subject_5 == 'Free':
                assign5.subject = None
                assign5.teacher = None
                assign5.save()
            else:
                subject_5 = Subjects.objects.get(id=subject_5)
                teacher_5 = Teacher.objects.get(id=teacher_5)
                assign5.subject = subject_5
                assign5.teacher = teacher_5
                assign5.save()
            return redirect('/admin-dashboard')
        else:
            pass
    else:
        messages.warning(request, 'Unauthorized Access!')
        return redirect('/dashboard')


@login_required
def AssignTimeTable(request):
    role = request.user.profile.role
    if role == 'admin':
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
            current = TimeTabel.objects.filter(day=day)
            current_timetable = []
            for i in current:
                current_timetable.append(i)
            data = {'days': days, 'subjects': subjects, 'time': time, 'day': day, 'current': current_timetable}
            return render(request, 'dashboard/add_time_table.html', data)
        else:
            return redirect('/add-subjects')
    else:
        messages.warning(request, 'Unauthorized Access!')
        return redirect('/dashboard')


@login_required
def addClass(request):
    role = request.user.profile.role
    if role == 'teacher':
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
                    added_on=added_on, date=my_date, zoom_link=zoom_link, time=time, cls=cls,
                    added_by=request.user.profile
                )
                Classes.objects.filter(date__lt=(date.today() - timedelta(days=2))).delete()
                messages.info(request, 'Zoom Link Added Successfully!')
            return redirect('/view-class')
        else:
            today = date.today()
            last_date = date.today() + timedelta(days=1)
            data = {'today': str(today), 'last_date': str(last_date)}
            return render(request, 'dashboard/teacher/classes.html', data)
    else:
        messages.warning(request, 'Unauthorized Access!')
        return redirect('/dashboard')


@login_required
def viewClass(request):
    role = request.user.profile.role
    if role == 'teacher':
        if request.method == 'POST':
            id = request.POST['id']
            zoom_link = request.POST['zoom_link']
            cls = Classes.objects.get(id=id)
            cls.zoom_link = zoom_link
            cls.save()
            messages.success(request, 'Edited Successfully')
            return redirect('/view-class')
        else:
            links = Classes.objects.filter(added_by=request.user.profile)
            data = {'links': links}
            return render(request, 'dashboard/teacher/view_classes.html', data)
    else:
        messages.warning(request, 'Unauthorized Access!')
        return redirect('/dashboard')


@login_required
def DeleteClassLink(request, i_id):
    role = request.user.profile.role
    if role == 'teacher':
        classs = Classes.objects.get(id=i_id)
        date = classs.date
        classs.delete()
        messages.success(request, 'classs ' + str(date) + ' deleted Successfully!')
        return redirect('/view-class')
    else:
        messages.warning(request, 'Unauthorized Access!')
        return redirect('/dashboard')


@login_required
def quizStudent(request):
    role = request.user.profile.role
    if role == 'student':
        student = request.user.profile.student
        try:
            done = QuizStudent.objects.filter(student_id=student.student_id)
            done = [i.subject_id for i in done]
            quiz_subjects = Quiz.objects.filter(
                start_date__lte=date.today(), end_date__gte=date.today()
            ).exclude(subject_id__in=done)
        except QuizStudent.DoesNotExist:
            quiz_subjects = Quiz.objects.filter(
                start_date__lte=date.today(), end_date__gte=date.today()
            )
        data = {'quiz_subjects': quiz_subjects, }
        return render(request, 'dashboard/student/quiz.html', data)
    else:
        messages.warning(request, 'Unauthorized Access!')
        return redirect('/dashboard')


@login_required
def quizStartStudent(request):
    role = request.user.profile.role
    if role == 'student':
        if request.method == "POST":
            id = request.POST['id']
            quiz = Quiz.objects.get(id=id)
            n = 0
            questions = QuizQuestion.objects.filter(quiz=quiz.id)
            q = []
            for i in questions:
                n += 1
                dic = {'n': n, 'q': i}
                q.append(dic)
            data = {'questions': q, 'n': n, 'quiz': quiz}
            return render(request, 'dashboard/student/start_quiz.html', data)
        else:
            messages.warning(request, 'Bad Request!')
            return redirect('/dashboard')
    else:
        messages.warning(request, 'Unauthorized Access!')
        return redirect('/dashboard')


@login_required
def quizSubmit(request):
    role = request.user.profile.role
    if role == 'student':
        student = request.user.profile.student
        if request.method == "POST":
            num = int(request.POST['num'])
            quiz_id = int(request.POST['quiz_id'])
            quiz = Quiz.objects.get(id=quiz_id)
            obtain = 0
            total = 0
            for i in range(1, num + 1):
                id = request.POST['id_' + str(i)]
                answer = request.POST['question_' + str(i)]
                question = QuizQuestion.objects.get(id=id)
                if answer == question.answer:
                    obtain += int(question.score)
                    total += int(question.score)
                    correct = True
                else:
                    total += int(question.score)
                    correct = False
                QuizAnswers.objects.create(
                    question_id=id, quiz_student=student.student_id, answer=answer,
                    correct=correct
                )
            QuizStudent.objects.create(
                student=student, student_id=student.student_id, subject=quiz.subject,
                subject_id=quiz.subject_id, total_score=total, obtain_score=obtain,
                date=date.today(), teacher=quiz.teacher, teacher_id=quiz.teacher_id
            )
            messages.info(request, 'Your Responses have been captured Successfully!')
            return redirect('/dashboard')
    else:
        messages.warning(request, 'Unauthorized Access!')
        return redirect('/dashboard')


@login_required
def quizTeacher(request):
    role = request.user.profile.role
    if role == 'teacher':
        profile = request.user.profile
        if request.method == "POST":
            subject_id = request.POST['subject']
            start = request.POST['start']
            end = request.POST['end']
            subject = Subjects.objects.get(id=subject_id).name
            Quiz.objects.create(
                subject_id=subject_id, subject=subject, created_date=date.today(),
                start_date=start, end_date=end, teacher=profile, teacher_id=profile.teacher.teacher_id,
            )
            messages.info(request, 'Quiz for ' + subject + ' Created Successfully!')
            return redirect('/quiz')
        else:
            subjects = TeacherSubjectAssign.objects.filter(teacher=profile.teacher)
            subject = []
            for i in subjects:
                subject.append(i.subject.id)
            quiz_subjects = Quiz.objects.filter(subject_id__in=subject)
            data = {'quiz_subjects': quiz_subjects, 'subjects': subjects}
            return render(request, 'dashboard/teacher/quiz.html', data)
    else:
        messages.warning(request, 'Unauthorized Access!')
        return redirect('/dashboard')


@login_required
def viewResults(request):
    role = request.user.profile.role
    if role == 'teacher':
        profile = request.user.profile
        result = QuizStudent.objects.filter(teacher_id=profile.teacher.teacher_id)
        data = {'results': result}
        return render(request, 'dashboard/teacher/results.html', data)


@login_required
def quizQuestion(request, id):
    role = request.user.profile.role
    if role == 'teacher':
        profile = request.user.profile
        if request.method == "POST":
            quiz = Quiz.objects.get(id=id)
            question = request.POST['question']
            option1 = request.POST['option1']
            option2 = request.POST['option2']
            option3 = request.POST.get('option3')
            option4 = request.POST.get('option4')
            answer = request.POST['answer']
            score = request.POST['score']
            QuizQuestion.objects.create(
                quiz=quiz.id, question=question, answer=answer, option_1=option1,
                option_2=option2, option_3=option3, option_4=option4, score=score,
                subject=quiz.subject, subject_id=quiz.subject_id,
                teacher=quiz.teacher, teacher_id=quiz.teacher_id
            )
            return redirect('/question/' + str(id))

        else:
            quiz = Quiz.objects.get(id=id)
            questions = QuizQuestion.objects.filter(quiz=quiz.id)
            data = {'questions': questions, 'quiz': quiz}
            return render(request, 'dashboard/teacher/question.html', data)
    else:
        messages.warning(request, 'Unauthorized Access!')
        return redirect('/dashboard')


@login_required
def quizeditQuestion(request, id):
    role = request.user.profile.role
    if role == 'teacher':
        profile = request.user.profile
        if request.method == "POST":
            quiz = request.POST['quiz']
            q = QuizQuestion.objects.get(id=id)
            teacher = q.quiz.teacher_id
            if teacher == profile.teacher.teacher_id:
                question = request.POST['question']
                option1 = request.POST['option1']
                option2 = request.POST['option2']
                option3 = request.POST.get('option3')
                option4 = request.POST.get('option4')
                answer = request.POST['answer']
                score = request.POST['score']
                q.question = question
                q.option_1 = option1
                q.option_2 = option2
                q.option_3 = option3
                q.option_4 = option4
                q.answer = answer
                q.score = score
                q.save()
                return redirect('/question/' + str(quiz))
            else:
                messages.warning(request, 'You are not authorized to delete this question!')
                return redirect('/question/' + str(quiz))


@login_required
def quizDeleteQuestion(request, id):
    role = request.user.profile.role
    if role == 'teacher':
        profile = request.user.profile
        q = QuizQuestion.objects.get(id=id)
        teacher = q.quiz.teacher_id
        quiz = q.quiz.id
        if teacher == profile.teacher.teacher_id:
            q.delete()
            return redirect('/question/' + str(quiz))
        else:
            messages.warning(request, 'You are not authorized to delete this question!')
            return redirect('/question/' + str(quiz))


@login_required
def selectSubject(request):
    role = request.user.profile.role
    if role == 'teacher':
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
                        dic[
                            'student'] = i.profile.first_name + ' ' + i.profile.second_name + ' ' + i.profile.third_name + ' ' + i.profile.last_name
                        dic['student_id'] = i.student_id
                        dic['id'] = att.id
                        dic['status'] = att.status
                    else:
                        dic[
                            'student'] = i.profile.first_name + ' ' + i.profile.second_name + ' ' + i.profile.third_name + ' ' + i.profile.last_name
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
    else:
        messages.warning(request, 'Unauthorized Access!')
        return redirect('/dashboard')


@login_required
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


@login_required
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


@login_required
def getSubject(request):
    id = request.POST['id']
    subject = Subjects.objects.get(id=id)
    teachers = TeacherSubjectAssign.objects.filter(subject=subject)
    teacher = []
    for i in teachers:
        dic = {}
        dic['id'] = i.teacher.id
        dic[
            'name'] = i.teacher.profile.first_name + " " + i.teacher.profile.second_name + " " + i.teacher.profile.third_name + " " + i.teacher.profile.last_name
        teacher.append(dic)
    return HttpResponse(json.dumps(teacher))


@login_required
def getTeacherSubject(request):
    day_date = request.POST['date']
    day_date = datetime.strptime(day_date, '%Y-%m-%d').weekday()
    day = calendar.day_name[day_date]
    time_table = TimeTabel.objects.filter(day=day, teacher=request.user.profile.teacher)
    time = []
    for i in time_table:
        time.append({'id': i.id, 'time': str(i.time), 'subject': str(i.subject)})
    return HttpResponse(json.dumps(time))


@login_required
def ViewTeacherSubjectAssign(request):
    role = request.user.profile.role
    if role == 'admin':
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
    else:
        messages.warning(request, 'Unauthorized Access!')
        return redirect('/dashboard')


@login_required
def createTimetable(request):
    password = request.GET.get('pass')
    if password == 'Najwa':
        for i in DAYS_OF_WEEK:
            for j in time_slots:
                try:
                    TimeTabel.objects.get(day=i[0], time=j[0])
                except TimeTabel.DoesNotExist:
                    TimeTabel.objects.create(
                        day=i[0], time=j[0]
                    )
        messages.info(request, 'Empty Timetable Created Successfully!')
        return redirect('/login')
    else:
        messages.info(request, 'Invalid Request!')
        return redirect('/login')

@login_required
def FrontEnd(request):
    if request.user.profile.role == 'admin':
        if request.method == 'POST':
            img = request.FILES.get('banner')
            num1 = request.POST['num1']
            num2 = request.POST['num2']
            num3 = request.POST['num3']
            num4 = request.POST['num4']
            e = FrontEndData.objects.first()
            if e:
                f = e
            else:
                f = FrontEndData()
            if img:
                f.img = img
            f.num1 = num1
            f.num2 = num2
            f.num3 = num3
            f.num4 = num4
            f.save()
            messages.success(request, 'Successfully added.')
            return redirect('/dashboard')
        else:
            f = FrontEndData.objects.first()
            data = {'f': f}
            return render(request, 'dashboard/frontend_data.html', data)
    else:
        messages.success(request, 'Invalid Request!')
        return redirect('/dashboard')


@login_required
def download_reports(request):
    if request.user.profile.role == 'admin':
        if request.method == 'POST':
            typee = request.POST['type']
            if typee == 'attendance':
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                student = request.POST['student']
                subject = request.POST['subject']
                columns = ['Date', 'Time', 'Student Name', 'Student Id', 'Subject', 'Marked by', 'Status']
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="' + str(
                    date.today()) + ' - Attendance Report.csv"'
                writer = csv.writer(response)
                writer.writerow(columns)
                if student == 'all' and subject == 'all':
                    query = Attendance.objects.filter(date__range=[start_date, end_date])
                elif student == 'all':
                    query = Attendance.objects.filter(date__range=[start_date, end_date], subject_id=subject)
                elif subject == 'all':
                    query = Attendance.objects.filter(date__range=[start_date, end_date], student_id=student)
                else:
                    query = Attendance.objects.filter(date__range=[start_date, end_date],
                                                      student_id=student, subject_id=subject)
                for i in query:
                    data = [
                        i.date, i.time, i.student, i.student_id, i.subject,
                        str(i.teacher) + ' (' + str(i.teacher_id) + ')', i.status
                    ]
                    writer.writerow(data)
                return response
            else:
                student = request.POST['student']
                subject = request.POST['subject']
                columns = ['Student Name', 'Student_id', 'Subject', 'Total Score', 'Obtained Score', 'Date of Answer']
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="' + str(date.today()) + ' - Marks Report.csv"'
                writer = csv.writer(response)
                writer.writerow(columns)
                if student == 'all' and subject == 'all':
                    query = QuizStudent.objects.all()
                elif student == 'all':
                    query = QuizStudent.objects.filter(subject_id=subject)
                elif subject == 'all':
                    query = QuizStudent.objects.filter(student_id=student)
                else:
                    query = QuizStudent.objects.filter(student_id=student, subject_id=subject)
                for i in query:
                    data = [
                        i.student, i.student_id, i.subject, i.total_score, i.obtain_score, i.date
                    ]
                    writer.writerow(data)
                return response
        else:
            students = Student.objects.all()
            subjects = Subjects.objects.all()
            data = {'students': students, 'subjects': subjects}
            return render(request, 'dashboard/downloads.html', data)
    else:
        messages.success(request, 'Invalid Request!')
        return redirect('/dashboard')


def send_email(request):
    name = request.POST['name']
    email = request.POST['email']
    message = request.POST['message']
    subject = 'رسالة جديدة من  '+str(name)
    try:
        email_template = "<table border='1'><tr><th>Name</th><td>" + str(
            name) + "</td></tr><tr><th>Email</th><td>" + str(email) + "</td></tr><tr><th>Message</th><td>" + str(
            message) + "</td></tr></table>"
        to = ['swms3902@gmail.com']
        email_msg = EmailMessage(subject,
                                 email_template, 'admin@innovatelifesciences.org',
                                 to,
                                 reply_to=[email])
        email_msg.content_subtype = 'html'
        email_msg.send(fail_silently=False)
        messages.success(request, 'تم إرسال رسالتك بنجاح')
    except:
        messages.success(request, 'حدث خطأ ما, يرجى التواصل مع عهذا الإيميل لمزيد من المعلومات swms3902@gmail.com')
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def add_testimonial(request):
    if request.user.profile.role == 'admin':
        if request.method == 'POST':
            name = request.POST['name']
            testimonial = request.POST.get('testimonial')
            designation = request.POST.get('designation')
            try:
                Testimonials.objects.create(
                    name=name, testimonial=testimonial, designation=designation
                )
                messages.success(request, 'تم إضافة التقييم بنجاح')
            except IntegrityError:
                messages.error(request, 'هذا التقييم موجود مسبقا')
            return redirect('/add-testimonial')
        else:
            testimonial = Testimonials.objects.all()
            data = {'testimonial': testimonial}
            return render(request, 'dashboard/add_testimonial.html', data)
    else:
        messages.success(request, 'اجراء خاطئ')
        return redirect('/dashboard')


@login_required
def delete_testimonial(request):
    if request.user.profile.role == 'admin':
        if request.method == 'POST':
            pk = request.POST['id']
            Testimonials.objects.get(id=pk).delete()
            return redirect('/add-testimonial')
        else:
            messages.error(request, 'اجراء خاطئ')
            return redirect('/add-testimonial')
    else:
        messages.error(request, 'اجراء خاطئ')
        return redirect('/dashboard')
