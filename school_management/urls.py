from django.contrib import admin
from django.urls import path
from students.views import student_list, add_student # Update this line
from django.contrib.auth import views as auth_views # Add this
from students.views import student_list, add_student, edit_student, delete_student # Update imports

urlpatterns = [
    path('admin/', admin.site.register),
    path('students/', student_list, name='student_list'), # Our new URL
    path('students/add/', add_student, name='add_student'), # New URL
    path('login/', auth_views.LoginView.as_view(template_name='students/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('students/edit/<int:pk>/', edit_student, name='edit_student'),
    path('students/delete/<int:pk>/', delete_student, name='delete_student'),
]