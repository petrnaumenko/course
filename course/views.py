from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Course, Lesson, Student, Teacher
from .serializers import (
    CourseSerializer,
    LessonSerializer,
    StudentSerializer,
    TeacherSerializer,
)
from .services import (
    add_student_to_course,
    add_student_to_course_evenly,
    get_available_courses_info,
    get_available_lessons_for_student,
    get_course_details,
    get_courses_info,
    is_course_available_to_student,
)


@api_view(['GET'])
def available_courses(request):
    courses_data = get_available_courses_info()
    return Response(courses_data)


@api_view(['GET'])
def available_lessons(request):
    course_uuid = request.query_params.get('course_uuid')
    student_uuid = request.query_params.get('student_uuid')

    if not course_uuid or not student_uuid:
        return Response(
            {'error': 'Both course_uuid and student_uuid are required.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    lessons = get_available_lessons_for_student(course_uuid, student_uuid)
    return Response({'lessons': lessons})


@api_view(['GET'])
def check_course_availability(request):
    course_uuid = request.query_params.get('course_uuid')
    student_uuid = request.query_params.get('student_uuid')

    if not course_uuid or not student_uuid:
        return Response(
            {'error': 'Both course_uuid and student_uuid are required.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        available = is_course_available_to_student(course_uuid, student_uuid)
        return Response({'available': available})
    except Course.DoesNotExist:
        return Response(
            {'error': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND
        )
    except Student.DoesNotExist:
        return Response(
            {'error': 'Student not found.'}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
def courses_info(request):
    info = get_courses_info()
    return Response(info)


@api_view(['GET'])
def course_details(request, course_uuid):
    course_info = get_course_details(course_uuid)
    if course_info:
        return Response(course_info)
    else:
        return Response(
            {'error': 'Course is not found!'}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
def add_student_to_course_view(request):
    student_uuid = request.data.get('student_uuid')
    course_uuid = request.data.get('course_uuid')

    if not student_uuid or not course_uuid:
        return Response(
            {'error': 'student_uuid and course_uuid must be provided.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        add_student_to_course(student_uuid, course_uuid)
        return Response(
            {'success': 'Student has been successfully added to the course.'}
        )
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(
            {'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def add_student_to_course_evenly_view(request):
    student_uuid = request.data.get('student_uuid')
    course_uuid = request.data.get('course_uuid')

    if not student_uuid or not course_uuid:
        return Response(
            {'error': 'student_uuid and course_uuid must be provided.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        add_student_to_course_evenly(student_uuid, course_uuid)
        return Response(
            {'success': 'Student has been successfully added to the course.'}
        )
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(
            {'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_teacher(request, uuid):
    try:
        teacher = Teacher.objects.get(uuid=uuid)
    except Teacher.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TeacherSerializer(teacher)
    return Response(serializer.data)


@api_view(['POST'])
def add_teacher(request):
    serializer = TeacherSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_teacher(request, uuid):
    try:
        teacher = Teacher.objects.get(uuid=uuid)
    except Teacher.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TeacherSerializer(teacher, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_teacher(request, uuid):
    try:
        teacher = Teacher.objects.get(uuid=uuid)
        teacher.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Teacher.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_student(request, uuid):
    try:
        student = Student.objects.get(uuid=uuid)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = StudentSerializer(student)
    return Response(serializer.data)


@api_view(['POST'])
def add_student(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_student(request, uuid):
    try:
        student = Student.objects.get(uuid=uuid)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = StudentSerializer(student, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_student(request, uuid):
    try:
        student = Student.objects.get(uuid=uuid)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_course(request, uuid):
    try:
        course = Course.objects.get(uuid=uuid)
    except Course.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CourseSerializer(course)
    return Response(serializer.data)


@api_view(['POST'])
def add_course(request):
    serializer = CourseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_course(request, uuid):
    try:
        course = Course.objects.get(uuid=uuid)
    except Course.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CourseSerializer(course, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_lesson(request, uuid):
    try:
        lesson = Lesson.objects.get(uuid=uuid)
    except Lesson.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = LessonSerializer(lesson)
    return Response(serializer.data)


@api_view(['POST'])
def add_lesson(request):
    serializer = LessonSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_lesson(request, uuid):
    try:
        lesson = Lesson.objects.get(uuid=uuid)
    except Lesson.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = LessonSerializer(lesson, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_lesson(request, uuid):
    try:
        lesson = Lesson.objects.get(uuid=uuid)
        lesson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Lesson.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
