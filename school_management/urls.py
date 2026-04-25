from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from students import views  # This imports all your student functions at once

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),

    # Student Management
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/<int:pk>/', views.student_profile, name='student_profile'),
    path('students/edit/<int:pk>/', views.edit_student, name='edit_student'),
    path('students/delete/<int:pk>/', views.delete_student, name='delete_student'),

    # Authentication (Login/Logout)
    path('login/', auth_views.LoginView.as_view(template_name='students/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('attendance/', views.take_attendance, name='take_attendance'),
    path('students/<int:pk>/pdf/', views.download_report_card, name='download_report'),
]