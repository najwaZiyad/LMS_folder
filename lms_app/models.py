from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class AutoUsername(models.Model):
    type = models.CharField(max_length=50)
    last = models.CharField(max_length=50)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150)
    second_name = models.CharField(max_length=150, null=True, blank=True)
    third_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    address = models.TextField()
    role = models.CharField(max_length=150)

class Teacher(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    teacher_id = models.CharField(max_length=50)
    experience = models.CharField(max_length=80, null=True, blank=True)
    subjects = models.TextField(null=True, blank=True)

class Subjects(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    teacher_id = models.TextField()