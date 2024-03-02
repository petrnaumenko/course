import uuid

from django.db import transaction
from django.db.models import Avg, Count, F

from .models import Course, Group, Lesson, Student, StudentGroup


def get_available_lessons_for_student(course_uuid, student_uuid):

    if not is_course_available_to_student(course_uuid, student_uuid):
        return []

    lessons = Lesson.objects.filter(course__course_uuid=course_uuid).values(
        'lesson_uuid', 'title', 'materials'
    )
    return list(lessons)


def is_course_available_to_student(course_uuid, student_uuid):

    # Проверяем, существует ли группа, связанная с данным курсом и студентом
    return StudentGroup.objects.filter(
        group__course__course_uuid=course_uuid, student=student_uuid
    ).exists()


def get_courses_info():
    # Получаем общее количество студентов на платформе для расчета процента приобретения продукта
    total_students = Student.objects.count()

    courses = Course.objects.all()

    courses_info = []
    for course in courses:
        # Рассчитываем процент приобретения продукта
        student_count = (
            StudentGroup.objects.filter(group__course=course)
            .values('student')
            .distinct()
            .count()
        )
        purchase_percentage = (
            (student_count * 100 / total_students) if total_students > 0 else 0
        )

        # Получаем все группы, связанные с курсом
        groups = Group.objects.filter(course=course)

        # Рассчитываем среднее количество студентов на группу
        average_students = 0
        if len(groups):
            average_students = int(student_count / len(groups))

        average_group_fill = average_students * 100 / course.max_students

        courses_info.append(
            {
                'course_uuid': course.course_uuid,
                'title': course.title,
                'student_count': student_count,
                'average_group_fill': average_group_fill,
                'purchase_percentage': purchase_percentage,
            }
        )

    return courses_info


def get_course_details(course_uuid):
    try:
        course = Course.objects.get(course_uuid=course_uuid)
        groups = Group.objects.filter(course=course)

        course_info = {'course_title': course.title, 'groups': []}

        for group in groups:
            group_info = {'group_name': group.name, 'students': []}
            student_groups = group.students.all()
            for student in student_groups:
                group_info['students'].append(
                    f'{student.first_name} {student.last_name}'
                )
            course_info['groups'].append(group_info)

        return course_info
    except Course.DoesNotExist:
        return None


def get_available_courses_info():
    courses = Course.objects.all()
    courses_info = []

    for course in courses:
        lesson_count = Lesson.objects.filter(course=course).count()
        courses_info.append(
            {
                'course_uuid': course.course_uuid,
                'title': course.title,
                'start_datetime': course.start_datetime.isoformat(),
                'cost': course.cost,
                'min_students': course.min_students,
                'max_students': course.max_students,
                'lesson_count': lesson_count,
            }
        )

    return courses_info


def _get_course_student(course_uuid, student_uuid):

    # Проверяем, что предоставленные UUID действительны
    if isinstance(course_uuid, str):
        try:
            course_uuid = uuid.UUID(course_uuid)
        except Exception:
            raise ValueError('The course_uuid is not valid.')

    if isinstance(student_uuid, str):
        try:
            student_uuid = uuid.UUID(student_uuid)
        except Exception:
            raise ValueError('The student_uuid is not valid.')

    # Получаем курс и студента по UUID
    course = Course.objects.select_for_update().get(course_uuid=course_uuid)
    student = Student.objects.get(student_uuid=student_uuid)

    # Проверяем, записан ли студент уже на курс
    if Group.objects.filter(course=course, students=student).exists():
        raise ValueError('The student is already enrolled in this course.')

    return course, student


def add_student_to_course(student_uuid, course_uuid):
    with transaction.atomic():
        course, student = _get_course_student(course_uuid, student_uuid)

        # Получаем группы для текущего курса
        groups = (
            Group.objects.filter(course=course)
            .annotate(student_count=Count('students'))
            .order_by('student_count')
        )

        # Если групп нет или в первой группе максимальное количество студентов, создаем новую группу
        if not len(groups):
            group = Group.objects.create(
                course=course, name=f'Курс: {course.title}; Группа 1'
            )
        else:
            group = groups.first()
            if group.students.count() >= course.max_students:
                num = groups.count() + 1  # Номер новой группы
                group = Group.objects.create(
                    course=course, name=f'Курс: {course.title}; Группа {num}'
                )

        # Добавляем студента в группу
        group.students.add(student)


def redistribute_students(groups, group):

    students = sum([sg.students.count() for sg in groups]) + 1

    # Рассчитываем, сколько студентов должно быть в каждой группе
    students_per_group = students // (len(groups) + 1)

    count = 1
    while count < students_per_group:
        for gr in groups:
            student = gr.students.all().last()
            gr.students.remove(student)
            group.students.add(student)
            count += 1


def add_student_to_course_evenly(student_uuid, course_uuid):
    with transaction.atomic():
        course, student = _get_course_student(course_uuid, student_uuid)

        # Получаем все группы курса и определяем группу с минимальным количеством студентов
        groups = (
            Group.objects.filter(course=course)
            .annotate(student_count=Count('students'))
            .order_by('student_count')
        )

        num = 1
        if not len(groups):
            # Если нет групп, создаем новую группу
            group = Group.objects.create(
                course=course, name=f'Курс: {course.title}; Группа {num}'
            )
            group.students.add(student)
        elif groups and groups.first().student_count >= course.max_students:
            # Если группа переполнена, создаем новую группу
            num = groups.count() + 1  # Номер новой группы
            group = Group.objects.create(
                course=course, name=f'Курс: {course.title}; Группа {num}'
            )
            group.students.add(student)
            redistribute_students(groups, group)
        else:
            # Иначе выбираем группу с наименьшим количеством студентов
            groups.first().students.add(student)
