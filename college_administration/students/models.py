from django.db import models

# Department
class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Course
class Course(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Faculty
class Faculty(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Subject
class Subject(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Student
class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.IntegerField(unique=True)
    email = models.EmailField()

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    subjects = models.ManyToManyField(Subject, blank=True)

    def __str__(self):
        return self.name
    
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.BooleanField()  # Present / Absent

    def __str__(self):
        return f"{self.student.name} - {self.date}"

class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    marks = models.IntegerField()

    def __str__(self):
        return f"{self.student.name} - {self.subject.name}"
    
    