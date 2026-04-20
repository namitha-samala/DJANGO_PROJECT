from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required   # ✅ ADD THIS
from .models import Student, Course, Department, Subject, Marks
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login

# =======================
# STUDENT LIST
# =======================
@login_required
# def student_list(request):
#     students = Student.objects.all()

#     student_data = []

#     for student in students:
#         marks = Marks.objects.filter(student=student)

#         student_data.append({
#             'student': student,
#             'marks': marks
#         })

#     total = students.count()

#     courses = Course.objects.all()
#     departments = Department.objects.all()

#     return render(request, 'student_list.html', {
#         'student_data': student_data,
#         'total': total,
#         'courses': courses,
#         'departments': departments,
#     })






def student_list(request):
    query = request.GET.get('q')

    students = Student.objects.all()

    if query:
        students = students.filter(
            name__icontains=query
        ) | students.filter(
            roll_no__icontains=query
        )

    student_data = []

    for student in students:
        marks = Marks.objects.filter(student=student)

        student_data.append({
            'student': student,
            'marks': marks
        })

    return render(request, 'student_list.html', {
        'student_data': student_data,
        'query': query
    })




# =======================
# ADD STUDENT
# =======================
@login_required
def add_student(request):
    courses = Course.objects.all()
    departments = Department.objects.all()
    subjects = Subject.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        roll_no = request.POST.get('roll_no')
        email = request.POST.get('email')
        course_id = request.POST.get('course')
        department_id = request.POST.get('department')
        subject_id = request.POST.get('subject')
        marks_value = request.POST.get('marks')

        if not course_id:
            return render(request, 'add_student.html', {
                'courses': courses,
                'departments': departments,
                'subjects': subjects,
                'error': 'Please select a course'
            })

        if Student.objects.filter(roll_no=roll_no).exists():
            return render(request, 'add_student.html', {
                'courses': courses,
                'departments': departments,
                'subjects': subjects,
                'error': 'Student with this Roll No already exists'
            })

        course = Course.objects.get(id=course_id)
        department = Department.objects.get(id=department_id) if department_id else None

        student = Student.objects.create(
            name=name,
            roll_no=roll_no,
            email=email,
            course=course,
            department=department
        )

        if subject_id and marks_value:
            subject = Subject.objects.get(id=subject_id)

            Marks.objects.update_or_create(
                student=student,
                subject=subject,
                defaults={'marks': marks_value}
            )

        return redirect('/students/add/')

    return render(request, 'add_student.html', {
        'courses': courses,
        'departments': departments,
        'subjects': subjects
    })


# =======================
# EDIT STUDENT
# =======================
@login_required
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)

    courses = Course.objects.all()
    departments = Department.objects.all()
    subjects = Subject.objects.all()

    mark = Marks.objects.filter(student=student).first()

    if request.method == 'POST':
        student.name = request.POST.get('name')
        student.roll_no = request.POST.get('roll_no')
        student.email = request.POST.get('email')

        course_id = request.POST.get('course')
        department_id = request.POST.get('department')

        if course_id:
            student.course = Course.objects.get(id=course_id)

        student.department = Department.objects.get(id=department_id) if department_id else None

        student.save()

        subject_id = request.POST.get('subject')
        marks_value = request.POST.get('marks')

        if subject_id and marks_value:
            subject = Subject.objects.get(id=subject_id)

            Marks.objects.update_or_create(
                student=student,
                subject=subject,
                defaults={'marks': marks_value}
            )

        return redirect('/students/')

    return render(request, 'add_student.html', {
        'student': student,
        'courses': courses,
        'departments': departments,
        'subjects': subjects,
        'mark': mark
    })


# =======================
# DELETE STUDENT
# =======================
@login_required
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect('/students/')

@login_required
def add_marks(request):
    students = Student.objects.all()
    subjects = Subject.objects.all()

    if request.method == 'POST':
        student_id = request.POST.get('student')
        subject_id = request.POST.get('subject')
        marks_value = request.POST.get('marks')

        student = Student.objects.get(id=student_id)
        subject = Subject.objects.get(id=subject_id)

        Marks.objects.update_or_create(
            student=student,
            subject=subject,
            defaults={'marks': marks_value}
        )

        return redirect('/marks/add/')

    return render(request, 'add_marks.html', {
        'students': students,
        'subjects': subjects
    })

from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    total_students = Student.objects.count()
    total_courses = Course.objects.count()
    total_marks = Marks.objects.all()

    avg_marks = 0
    if total_marks.exists():
        avg_marks = sum(m.marks for m in total_marks) / total_marks.count()

    top_student = None
    if total_marks.exists():
        top = total_marks.order_by('-marks').first()
        top_student = top.student

    return render(request, 'dashboard.html', {
        'total_students': total_students,
        'total_courses': total_courses,
        'avg_marks': avg_marks,
        'top_student': top_student
    })

def logout_view(request):
    logout(request)
    return redirect('/login/')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # 🔒 Check passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('/register/')

        # 🔒 Check if user exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('/register/')

        # ✅ Create user
        User.objects.create_user(username=username, password=password)
        messages.success(request, "Account created successfully!")

        return redirect('/login/')

    return render(request, 'register.html')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')  # go to dashboard
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')