from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout

#
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
        Profile.objects.create(
            user=user, first_name=name1, second_name=name2, third_name=name3, last_name=name4,
            address=address, role=role
        )
        if role == 'teacher':
           last = AutoUsername.objects.get(type='Teacher')
        else:
           last = AutoUsername.objects.get(type='Student')
        last.last = int(last.last) + 1
        last.save()
        return redirect('/add-user')
        # if role == 'teacher':
        #     role = request.POST['role']
        #     role = request.POST['role']
        #     role = request.POST['role']
        #     role = request.POST['role']
    else:
        teacher = AutoUsername.objects.get(type='Teacher').last
        student = AutoUsername.objects.get(type='Student').last
        data = {'teacher': teacher, 'student': student}
        return render(request, 'dashboard/add_user.html', data)

