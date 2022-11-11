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
    img = models.ImageField(upload_to='users/', default="users/default.png")
    address = models.TextField()
    role = models.CharField(max_length=150)

    def __str__(self):
        return str(self.first_name) + " " + str(self.second_name) + " " + str(self.third_name) + " " + str(
            self.last_name)


class Teacher(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    teacher_id = models.CharField(max_length=50)
    experience = models.CharField(max_length=80, null=True, blank=True)
    subject = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.profile.first_name) + " " + str(self.profile.second_name) + " " + str(
            self.profile.third_name) + " " + str(self.profile.last_name)


class Student(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=50)

    def __str__(self):
        return str(self.profile.first_name) + " " + str(self.profile.second_name) + " " + str(
            self.profile.third_name) + " " + str(self.profile.last_name)


class Subjects(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.name


class TeacherSubjectAssign(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)


class TimeTabel(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.ForeignKey(Subjects, on_delete=models.SET_NULL, null=True, blank=True)
    subject_alt = models.CharField(max_length=100, null=True, blank=True)
    day = models.CharField(max_length=20, choices=DAYS_OF_WEEK)
    time = models.CharField(max_length=50, choices=time_slots)


class Classes(models.Model):
    added_on = models.DateTimeField()
    added_by = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    cls = models.CharField(max_length=200)
    time = models.CharField(max_length=100, choices=time_slots)
    zoom_link = models.CharField(max_length=200)
    status = models.BooleanField(default=False)


class Attendance(models.Model):
    date = models.DateField()
    time = models.CharField(max_length=150)
    marked_on = models.DateTimeField(null=True, blank=True)
    student = models.CharField(max_length=150)
    student_id = models.CharField(max_length=150)
    teacher = models.CharField(max_length=150)
    teacher_id = models.CharField(max_length=150)
    subject = models.CharField(max_length=150)
    subject_id = models.CharField(max_length=150, null=True, blank=True)
    status = models.CharField(max_length=100)


# Assignment / Quiz
class Quiz(models.Model):
    created_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    teacher = models.CharField(max_length=200, null=True)
    teacher_id = models.CharField(max_length=50, null=True)
    subject = models.CharField(max_length=200)
    subject_id = models.CharField(max_length=20)


class QuizQuestion(models.Model):
    quiz = models.CharField(max_length=20)
    subject = models.CharField(max_length=200, null=True, blank=True)
    subject_id = models.CharField(max_length=20, null=True, blank=True)
    teacher = models.CharField(max_length=200, null=True, blank=True)
    teacher_id = models.CharField(max_length=50, null=True, blank=True)
    question = models.TextField()
    answer = models.TextField()
    option_1 = models.TextField()
    option_2 = models.TextField()
    option_3 = models.TextField(null=True, blank=True)
    option_4 = models.TextField(null=True, blank=True)
    score = models.CharField(max_length=20)


class QuizStudent(models.Model):
    quiz_id = models.CharField(max_length=20, null=True, blank=True)
    student = models.CharField(max_length=150)
    student_id = models.CharField(max_length=50)
    teacher = models.CharField(max_length=200, null=True, blank=True)
    teacher_id = models.CharField(max_length=50, null=True, blank=True)
    subject = models.CharField(max_length=150)
    subject_id = models.CharField(max_length=20)
    total_score = models.CharField(max_length=50)
    obtain_score = models.CharField(max_length=50)
    date = models.DateField(null=True, blank=True)


class QuizAnswers(models.Model):
    question_id = models.CharField(max_length=50)
    quiz_student = models.CharField(max_length=50)
    answer = models.TextField()
    correct = models.BooleanField()


class FrontEndData(models.Model):
    img = models.ImageField(upload_to='banner', default='banner/banner.png')
    num1 = models.CharField(max_length=50)
    num2 = models.CharField(max_length=50)
    num3 = models.CharField(max_length=50)
    num4 = models.CharField(max_length=50)


class Testimonials(models.Model):
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200, null=True, blank=True)
    testimonial = models.TextField()
