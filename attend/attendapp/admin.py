from django.contrib import admin
from attendapp.models import Teachers, Students, Attendance

# Register your models here.
admin.site.register(Teachers)
admin.site.register(Students)
admin.site.register(Attendance)
