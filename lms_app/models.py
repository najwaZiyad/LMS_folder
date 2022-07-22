from django.contrib.auth.models import User
from django.db import models

# Create your models here.


time_slots = (
    ('7:00 - 7:30', '7:00 - 7:30'),
    ('7:30 - 8:05', '7:30 - 8:05'),
    ('8:05 - 8:45', '8:05 - 8:45'),
    ('8:45 - 9:00', '8:45 - 9:00'),
    ('9:00 - 9:15', '9:00 - 9:15'),
)
DAYS_OF_WEEK = (
    ('Sunday', 'Sunday'),
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
)

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

    def __str__(self):
        return self.user.username

class Teacher(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    teacher_id = models.CharField(max_length=50)
    experience = models.CharField(max_length=80, null=True, blank=True)
    subject = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.profile.first_name

class Subjects(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    def __str__(self):
        return self.name

class TeacherSubjectAssign(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)

class TimeTabel(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, null=True, blank=True)
    subject_alt = models.CharField(max_length=100, null=True, blank=True)
    day = models.CharField(max_length=20, choices=DAYS_OF_WEEK)
    time = models.CharField(max_length=50, choices=time_slots)

class Classes(models.Model):
    added_on = models.DateTimeField()
    date = models.DateField()
    cls = models.CharField(max_length=200)
    time = models.CharField(max_length=100, choices=time_slots)
    zoom_link = models.CharField(max_length=200)
    status = models.BooleanField(default=False)
