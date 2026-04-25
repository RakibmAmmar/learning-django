from django.db import models

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    enrollment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Notice how 'class Grade' starts at the very beginning of the line below:
class Grade(models.Model):
    # This links the grade to a specific student
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    subject = models.CharField(max_length=100)
    score = models.PositiveIntegerField()
    date_assigned = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject}: {self.score}"
    
class Attendance(models.Model):
    STATUS_CHOICES = (
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('student', 'date') # Prevents double-marking a student on the same day

    def __str__(self):
        return f"{self.student.first_name} - {self.date} - {self.status}"