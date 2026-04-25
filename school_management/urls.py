from django.contrib import admin
from django.urls import path
from students.views import student_list, add_student # Update this line

urlpatterns = [
    path('admin/', admin.site.register),
    path('students/', student_list, name='student_list'), # Our new URL
    path('students/add/', add_student, name='add_student'), # New URL
]