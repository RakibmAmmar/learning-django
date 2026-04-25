from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from datetime import date
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template

# Import your models and forms
from .models import Student, Grade, Attendance
from .forms import StudentForm, GradeForm

@login_required
def student_list(request):
    query = request.GET.get('search')
    if query:
        all_students = Student.objects.filter(
            models.Q(first_name__icontains=query) | 
            models.Q(last_name__icontains=query)
        )
    else:
        all_students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': all_students})

@login_required
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student added successfully!")
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'students/add_student.html', {'form': form})

@login_required
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully!")
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/add_student.html', {'form': form, 'edit_mode': True})

@login_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        messages.error(request, "Student has been deleted.")
        return redirect('student_list')
    return render(request, 'students/delete_confirm.html', {'student': student})

@login_required
def student_profile(request, pk):
    student = get_object_or_404(Student, pk=pk)
    grades = student.grades.all()
    
    # Calculate Attendance Percentage for the Dashboard
    total_days = student.attendance.count()
    present_days = student.attendance.filter(status='Present').count()
    attendance_percent = (present_days / total_days * 100) if total_days > 0 else 0
    
    if request.method == "POST":
        form = GradeForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.student = student
            grade.save()
            messages.success(request, f"Grade added for {student.first_name}")
            return redirect('student_profile', pk=student.pk)
    else:
        form = GradeForm()
        
    return render(request, 'students/student_profile.html', {
        'student': student, 
        'grades': grades, 
        'form': form,
        'attendance_percent': round(attendance_percent, 1)
    })

@login_required
def take_attendance(request):
    students = Student.objects.all()
    today = date.today()
    
    if request.method == "POST":
        for student in students:
            status = request.POST.get(f"status_{student.id}")
            if status:
                Attendance.objects.update_or_create(
                    student=student, 
                    date=today, 
                    defaults={'status': status}
                )
        messages.success(request, f"Attendance for {today} saved successfully!")
        return redirect('student_list')

    return render(request, 'students/attendance.html', {'students': students, 'today': today})


def download_report_card(request, pk):
    student = get_object_or_404(Student, pk=pk)
    grades = student.grades.all()
    
    # Calculate Attendance for the report
    total_days = student.attendance.count()
    present_days = student.attendance.filter(status='Present').count()
    attendance_percent = (present_days / total_days * 100) if total_days > 0 else 0

    template_path = 'students/report_card_pdf.html'
    context = {
        'student': student,
        'grades': grades,
        'attendance': round(attendance_percent, 1),
        'today': date.today(),
    }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{student.last_name}_Report.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)

    # Create the PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response