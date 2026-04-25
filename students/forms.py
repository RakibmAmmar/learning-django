from django import forms
from .models import Student
from .models import Student, Grade # Add Grade here

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email']

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['subject', 'score']        