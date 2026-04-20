# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.student_list, name='student_list'),
#     path('students/add/', views.add_student, name='add_student'),
#     path('add/', views.add_student, name='add_student'),
#     path('edit/<int:id>/', views.edit_student, name='edit_student'),
#     path('delete/<int:id>/', views.delete_student, name='delete_student'),
# ]









from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.add_student, name='add_student'),  # ✅ ADD THIS
    path('students/edit/<int:id>/', views.edit_student, name='edit_student'),
    path('students/delete/<int:id>/', views.delete_student, name='delete_student'),
    path('marks/add/', views.add_marks, name='add_marks'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
]