from django.urls import URLPattern, path
from attendapp import views

urlpatterns = [
    path('attendapp/',views.attendapp, name='attenapp'),
    path('register/',views.teach_register,name='register'),
    path('login/',views.teach_login, name='login'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('student/',views.student, name='student'),
    path('attendance/',views.attendance, name='attendance'),
    path('display/',views.display_data, name='display'),
    path('view_students/',views.view_students, name='view_students'),
    path('edit_student/<int:id>/',views.edit_student, name='edit_student'),
    path('view_attendance/',views.view_attendance, name='view_attendance'),
    path('edit_attendance/<int:id>',views.edit_attendance, name='edit_attendance'),
   

]
