import calendar
from datetime import datetime, timedelta
from email import message
from multiprocessing import context
from tracemalloc import start
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from attendapp.models import Attendance, Teachers, Students
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.contrib.auth.models import User



# Create your views here.
def dashboard(request):
    today = datetime.today().date()
    start_date = today.replace(day=1)
    last_day_of_month = calendar.monthrange(today.year, today.month)[1]
    end_date = today.replace(day=last_day_of_month)

    dates = Attendance.objects.filter(date__range=(start_date, end_date)).exclude(date__week_day=1).values_list('date', flat=True).distinct().order_by('date')
    dates = [date.strftime('%Y-%m-%d') for date in dates]
    
    students = Students.objects.all()
    attend_data = []

    student_names = []
    attendance_percentages = []

    for student in students:
        student_data = {
            'id': student.id,
            'name': student.student_name,
            'attendance': [],
            'percentage': 0  # Initialize percentage
        }
        for date in dates:
            attend_record = Attendance.objects.filter(student=student, date=date).first()
            status = attend_record.status if attend_record else '-'
            student_data['attendance'].append(status)
        
        attendance_percentage = calculate_attendance_percentage(student.id, start_date, end_date)
        student_data['percentage'] = round(attendance_percentage, 2)
        
        attend_data.append(student_data)
        student_names.append(student.student_name)
        attendance_percentages.append(round(attendance_percentage, 2))

    context = {
        'dates': dates,
        'attend_data': attend_data,
        'student_names': student_names,
        'attendance_percentages': attendance_percentages,
    }
    return render(request, 'dash.html', context)
    

def attendapp(request):
    return render(request,'register.html')

def teach_register(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        contact=request.POST['contact']
        address=request.POST['address']

        use= Teachers.objects.filter(email=email)
        if use.exists():
            messages.info(request,"User already exists")
            print("user exists")
            return render(request,'register.html')
        if password != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Create the Teacher profile
        Teachers.objects.create(user=user,username=username,email=email,password=password, contact=contact, address=address)
        
        messages.success(request, "Registration successful.")
        return redirect('login')

    return render(request, 'register.html')
       
def teach_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, email=email, password=password)
        if user is None:
            messages.error(request, "Invalid email or password")
            return render(request, 'login.html')
        else:
            # Log in the user and redirect to the home page upon successful login
            login(request, user)
            return redirect('dashboard')
    
    return render(request, 'login.html')

def student(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        student_name = request.POST.get('student_name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        gender = request.POST.get('gender')

        print(f"id: {id}, student_name: {student_name}, email: {email}, contact: {contact}, gender: {gender}")


        # Check if all fields are filled
        if not student_name or not email or not contact or not gender:
            messages.error(request, "All fields are required.")
            return render(request, 'student.html')

        # Create and save the student record
        stud = Students(
            id=id,
            student_name=student_name,
            email=email,
            contact=contact,
            gender=gender
        )
        stud.save()
        messages.success(request, "Student data saved successfully")
        print("success")
        return redirect('view_students')  # Redirect to avoid form resubmission
    
    return render(request,'student.html')

def attendance(request):
    students = Students.objects.all()
    if request.method =='POST':
        date = request.POST.get('date',timezone.now().date())
        for student in students:
            status = request.POST.get(f'status_{student.id}')

            if not Attendance.objects.filter(student=student, date=date).exists():
                attend=Attendance(student=student,
                              date=date,
                              status=status)
                attend.save()
                messages.success(request,"Attendance record successfully")
            
            else:
                messages.warning(request,f"Attendance for {student.student_name} is already saved")
        return redirect('attendance')
    return render(request, 'attendance.html',{'students': students})

def display_data(request):
    students= Students.objects.all()
    attendance = Attendance.objects.filter(date=timezone.now().date())
    context= {
        'students' :students,
        'attendance':attendance,
        'today':timezone.now().date()
    }
    return render(request, 'display.html',context)

def view_students(request):
    students=Students.objects.all()
    context={'students':students}
    return render(request,'view_student.html',context)

def edit_student(request, id):
    student = get_object_or_404(Students,id=id)
    if request.method=="POST":
        student.student_name=request.POST.get('student_name')
        student.email=request.POST.get('email')
        student.contact=request.POST.get('contact')
        student.gender=request.POST.get('gender')

        if not student.student_name or not student.email or not student.contact or not student.gender:
            messages.error(request, "All fields are required.")
            return render(request, 'edit_student.html', {'student': student})
        student.save()
        messages.success(request, "Student data updated successfully")
        return redirect('view_students')
    
    return render(request,'edit_student.html')



def percentage(present_days, total_days):
    return (present_days / total_days) * 100 if total_days > 0 else 0

def calculate_attendance_percentage(student_id, start_date, end_date):
    present_days = Attendance.objects.filter(student_id=student_id, status='Present', date__range=(start_date, end_date)).count()
    
    total_days = 0
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() != 6:  
            total_days += 1
        current_date += timedelta(days=1)
    
    return percentage(present_days, total_days)

def view_attendance(request):
    today = datetime.today().date()
    start_date = today.replace(day=1)
    last_day_of_month = calendar.monthrange(today.year, today.month)[1]
    end_date = today.replace(day=last_day_of_month)

    dates = Attendance.objects.filter(date__range=(start_date, end_date)).exclude(date__week_day=1).values_list('date', flat=True).distinct().order_by('date')
    dates = [date.strftime('%Y-%m-%d') for date in dates]
    
    students = Students.objects.all()
    attend_data = []

    for student in students:
        student_data = {
            'id': student.id,
            'name': student.student_name,
            'attendance': [],
            'percentage': 0  # Initialize percentage
        }
        for date in dates:
            attend_record = Attendance.objects.filter(student=student, date=date).first()
            status = attend_record.status if attend_record else '-'
            student_data['attendance'].append(status)
        
        attendance_percentage = calculate_attendance_percentage(student.id, start_date, end_date)
        student_data['percentage'] = round(attendance_percentage, 2)
        
        attend_data.append(student_data)

    context = {
        'students': students,
        'dates': dates,
        'attend_data': attend_data,
    }
    return render(request, 'view_attendance.html', context)


def edit_attendance(request,id):
    attendance= get_object_or_404(Attendance, id=id)
    if request.method=='POST':
        attendance.status=request.POST.get('status')

        if not attendance.status:
            messages.error(request,'Status is required')
            return render(request,'edit.attendance.html',{'attendance':attendance})
        attendance.save()
        messages.success(request, "Attendance record updated successfully")
        return redirect('display')
    return render(request,'edit_attendance.html',{'attendance':attendance})


