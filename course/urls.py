"""
URL configuration for course project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from .views import (
    add_course,
    add_lesson,
    add_student,
    add_student_to_course_evenly_view,
    add_student_to_course_view,
    add_teacher,
    available_courses,
    available_lessons,
    check_course_availability,
    course_details,
    courses_info,
    delete_lesson,
    delete_student,
    delete_teacher,
    get_course,
    get_lesson,
    get_student,
    get_teacher,
    update_course,
    update_lesson,
    update_student,
    update_teacher,
)

urlpatterns = [
    path(
        'course/check-student-availability/',
        check_course_availability,
        name='check-course-availability',
    ),
    path(
        'course/available-courses/',
        available_courses,
        name='available-courses',
    ),
    path(
        'course/student-available-lessons/',
        available_lessons,
        name='available-lessons',
    ),
    path(
        'course/add-student/',
        add_student_to_course_view,
        name='add_student_to_course',
    ),
    path(
        'course/add-student-evenly/',
        add_student_to_course_evenly_view,
        name='add_student_to_course_evenly',
    ),
    path('course/total-info/', courses_info, name='courses-info'),
    path(
        'course/course-details/<uuid:course_uuid>/',
        course_details,
        name='course-details',
    ),
    path('teacher/<uuid:uuid>/', get_teacher, name='get_teacher'),
    path('teacher/add/', add_teacher, name='add_teacher'),
    path('teacher/update/<uuid:uuid>/', update_teacher, name='update_teacher'),
    path('teacher/delete/<uuid:uuid>/', delete_teacher, name='delete_teacher'),
    path('student/<uuid:uuid>/', get_student, name='get_student'),
    path('student/add/', add_student, name='add_student'),
    path('student/update/<uuid:uuid>/', update_student, name='update_student'),
    path('student/delete/<uuid:uuid>/', delete_student, name='delete_student'),
    path('lesson/<uuid:uuid>/', get_lesson, name='get_lesson'),
    path('lesson/add/', add_lesson, name='add_lesson'),
    path('lesson/update/<uuid:uuid>/', update_lesson, name='update_lesson'),
    path('lesson/delete/<uuid:uuid>/', delete_lesson, name='delete_lesson'),
    path('course/<uuid:uuid>/', get_course, name='get_course'),
    path('course/add/', add_course, name='add_course'),
    path('course/update/<uuid:uuid>/', update_course, name='update_course'),
]
