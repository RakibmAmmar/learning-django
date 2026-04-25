from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Student
from django.shortcuts import render, redirect # Add redirect here
from .forms import StudentForm # Add this import
from django.shortcuts import get_object_or_404 # Add this to your imports at the top
from django.db import models
from django.contrib import messages # Add this import

def student_list(request):
    query = request.GET.get('search')
    if query:
        # This filters students whose first name OR last name contains the search text
        all_students = Student.objects.filter(
            models.Q(first_name__icontains=query) | 
            models.Q(last_name__icontains=query)
        )
    else:
        all_students = Student.objects.all()
    
    return render(request, 'students/student_list.html', {'students': all_students})
@login_required # This is the guard!
def add_student(request):
    
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student added successfully!") # Add this
            return redirect('student_list') # Go back to the list after saving
        
    else:
        form = StudentForm()
    return render(request, 'students/add_student.html', {'form': form})

@login_required
def edit_student(request, pk):
    # This finds the specific student by their unique ID (pk)
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully!") # Add this
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/add_student.html', {'form': form, 'edit_mode': True})

@login_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        messages.error(request, "Student has been deleted.") # Add this (using error for red color)
        return redirect('student_list')
    return render(request, 'students/delete_confirm.html', {'student': student})