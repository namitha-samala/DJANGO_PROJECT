from django.contrib import admin
from .models import Student, Course, Department, Faculty
from .models import Subject, Attendance
from .models import Marks

admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Department)

admin.site.register(Faculty)

admin.site.register(Subject)
admin.site.register(Attendance)
admin.site.register(Marks) 