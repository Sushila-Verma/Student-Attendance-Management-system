from random import choices
from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Teachers(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, default='')
    username=models.CharField(max_length=255,default='')
    password=models.CharField(max_length=255,default='')
    email = models.EmailField(unique=True)
    contact= models.CharField(max_length=255)
    address= models.CharField(max_length=255)
    def __str__(self):
        return self.username
    
class Students(models.Model):
    id = models.IntegerField(primary_key=True)
    student_name= models.CharField(max_length=255)
    email = models.EmailField(default='as@gmail.com')
    contact= models.CharField(max_length=255)
    gender=models.CharField(max_length=255, default='')

    def __str__(self):
        return self.student_name


class Attendance(models.Model):
    student = models.ForeignKey(Students, on_delete=models.SET_NULL, null=True)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=15, choices=[('Present','Present'),('Absent','Absent')])

    def __str__(self):
        return f"{self.student.id} - {self.student.student_name}"