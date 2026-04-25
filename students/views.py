from django.shortcuts import render
from .models import Student
from django.shortcuts import render, redirect # Add redirect here
from .forms import StudentForm # Add this import

def student_list(request):
    # This line grabs ALL students from the database
    all_students = Student.objects.all()
    # This line sends those students to an HTML file (template)
    return render(request, 'students/student_list.html', {'students': all_students})

def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list') # Go back to the list after saving
    else:
        form = StudentForm()
    return render(request, 'students/add_student.html', {'form': form})