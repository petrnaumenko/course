#!/usr/bin/env python
"""Курс демо файл"""
import time
import uuid

import requests


class CourseManager:
    API_BASE_URL = 'http://localhost:8000'

    def __init__(
        self,
        title,
        cost,
        num_students,
        num_lessons,
        min_students,
        max_students,
    ):
        self.title = title
        self.cost = cost
        self.num_students = num_students
        self.num_lessons = num_lessons
        self.min_students = min_students
        self.max_students = max_students
        self.course_uuid = uuid.uuid4()
        self.student_uuids = {}

    def add_teacher(self, first_name, last_name):
        teacher_uuid = uuid.uuid4()
        response = requests.post(
            f'{self.API_BASE_URL}/teacher/add/',
            json={
                'teacher_uuid': str(teacher_uuid),
                'first_name': first_name,
                'last_name': last_name,
            },
        )
        return teacher_uuid, response

    def add_course(self, start_datetime, teacher_uuid):
        response = requests.post(
            f'{self.API_BASE_URL}/course/add/',
            json={
                'course_uuid': str(self.course_uuid),
                'title': self.title,
                'start_datetime': start_datetime,
                'cost': self.cost,
                'min_students': self.min_students,
                'max_students': self.max_students,
                'teachers': [str(teacher_uuid)],
            },
        )
        return response

    def add_lessons(self):
        for i in range(1, self.num_lessons + 1):
            lesson_uuid = uuid.uuid4()
            response = requests.post(
                f'{self.API_BASE_URL}/lesson/add/',
                json={
                    'lesson_uuid': str(lesson_uuid),
                    'course': str(self.course_uuid),
                    'title': f'Урок {i}',
                    'materials': f'Материалы для урока {i}',
                },
            )

    def _add_students_to_db(self):
        for i in range(1, self.num_students + 1):
            student_uuid = uuid.uuid4()
            student_info = {
                'student_uuid': str(student_uuid),
                'first_name': f'Студент {i}',
                'last_name': f'Фамилия {i}',
            }
            response = requests.post(
                f'{self.API_BASE_URL}/student/add/', json=student_info
            )
            self.student_uuids[student_uuid] = student_info

    def add_students_to_course(self):
        self._add_students_to_db()
        for student_uuid in self.student_uuids:
            response = requests.post(
                f'{self.API_BASE_URL}/course/add-student/',
                json={
                    'student_uuid': str(student_uuid),
                    'course_uuid': str(self.course_uuid),
                },
            )

    def add_students_to_course_evenly(self):
        self._add_students_to_db()
        for student_uuid in self.student_uuids:
            response = requests.post(
                f'{self.API_BASE_URL}/course/add-student-evenly/',
                json={
                    'student_uuid': str(student_uuid),
                    'course_uuid': str(self.course_uuid),
                },
            )

    def print_course_details(self):
        # Строим URL для запроса
        url = f'{self.API_BASE_URL}/course/course-details/{self.course_uuid}/'

        # Выполняем GET-запрос
        response = requests.get(url)

        # Проверяем, успешно ли выполнен запрос
        if response.status_code == 200:
            # Разбираем JSON-ответ
            course_info = response.json()

            # Печатаем информацию о курсе
            print(f"Название курса: {course_info['course_title']}")
            for group in course_info['groups']:
                print(f"\nГруппа: {group['group_name']}")
                print('Студенты:')
                pn = 1
                for student in group['students']:
                    print(f' {pn}. {student}')
                    pn += 1
        else:
            print(
                'Информация о курсе не найдена или произошла ошибка при запросе.'
            )

    def print_courses_info(self):
        # Строим URL для запроса
        url = f'{self.API_BASE_URL}/course/total-info/'

        # Выполняем GET-запрос
        response = requests.get(url)

        courses = response.json()

        for course in courses:
            print(f"Курс: {course['title']}")
            print(f"UUID курса: {course['course_uuid']}")
            print(f"Количество студентов: {course['student_count']}")
            print(
                f"Среднее заполнение групп: {course['average_group_fill']:.2f}%"
            )
            print(
                f"Процент приобретения: {course['purchase_percentage']:.2f}%"
            )
            print('-' * 40)  # Разделитель между курсами

    def check_stdent_access(self, student_uuid, student_info):
        # Строим URL для запроса

        print(f"UUID студента: {student_info['student_uuid']}")
        print(f"Имя: {student_info['first_name']}")
        print(f"Фамилия: {student_info['last_name']}")

        url = f'{self.API_BASE_URL}/course/check-student-availability/?course_uuid={self.course_uuid}&student_uuid={student_uuid}'

        # Выполняем GET-запрос
        response = requests.get(url)

        # Проверяем, успешно ли выполнен запрос
        if response.status_code == 200:
            availability_info = response.json()
            # Вывод информации о курсе
            print(f'Курс: {self.title}')

            # Вывод информации о доступности
            print(
                f"Статус: {'Доступен' if availability_info['available'] else 'Не доступен'}"
            )
        else:
            print(
                'Информация о пользователе не найдена или произошла ошибка при запросе.'
            )

    def get_available_courses(self):
        # Строим URL для запроса

        url = f'{self.API_BASE_URL}/course/available-courses/'

        # Выполняем GET-запрос
        response = requests.get(url)

        # Проверяем, успешно ли выполнен запрос
        if response.status_code == 200:
            courses = response.json()
            for course in courses:
                print(f"Название курса: {course['title']}")
                print(f"UUID курса: {course['course_uuid']}")
                print(f"Дата и время начала: {course['start_datetime']}")
                print(f"Стоимость: {course['cost']}")
                print(
                    f"Минимальное количество студентов: {course['min_students']}"
                )
                print(
                    f"Максимальное количество студентов: {course['max_students']}"
                )
                print(f"Количество уроков: {course['lesson_count']}")
                print('-' * 60)
        else:
            print(
                'Информация о курсах не найдена или произошла ошибка при запросе.'
            )

    def get_available_lessons(self, student_uuid):
        # Строим URL для запроса

        url = f'{self.API_BASE_URL}/course/student-available-lessons/?course_uuid={self.course_uuid}&student_uuid={student_uuid}'

        # Выполняем GET-запрос
        response = requests.get(url)

        # Проверяем, успешно ли выполнен запрос
        if response.status_code == 200:
            lessons = response.json()
            for lesson in lessons['lessons']:
                print(f"Название урока: {lesson['title']}")
                print(f"UUID урока: {lesson['lesson_uuid']}")
                print(f"Материалы: {lesson['materials']}")
                print('-' * 50)  # Разделитель между уроками
        else:
            print(
                'Информация об уроках не найдена или произошла ошибка при запросе.'
            )


def main():
    print('Начало создания курсов...')

    # Создание курса "Основы Python"
    python_params = {
        'title': 'Основы Python',
        'cost': 12000,
        'num_students': 170,
        'num_lessons': 15,
        'min_students': 7,
        'max_students': 11,
    }
    print(
        f"\nСоздание курса '{python_params['title']}' с параметрами: \nстоимость - {python_params['cost']}, "
        f"\nчисло студентов - {python_params['num_students']}, \nчисло уроков - {python_params['num_lessons']}, "
        f"\nмин./макс. количество студентов в группе - {python_params['min_students']}/{python_params['max_students']}."
    )
    course_manager_python = CourseManager(**python_params)
    teacher_uuid_python, _ = course_manager_python.add_teacher(
        'Иван', 'Иванов'
    )
    print(f'\nПреподаватель Иван Иванов добавлен.')
    _ = course_manager_python.add_course(
        '2023-01-01T09:00:00Z', teacher_uuid_python
    )
    course_manager_python.add_lessons()
    print(f'\nУроки добавлены.')

    print(
        f'\nДобавляем студентов на курс по первому алгоритму: группа заполняется полностью, открывается/заполняется следующая и т.д.'
    )
    course_manager_python.add_students_to_course()

    print('\nВыводим распределение студентов по группам.')
    time.sleep(5)
    course_manager_python.print_course_details()

    # Создание курса "Основы C#"
    csharp_params = {
        'title': 'Основы C#',
        'cost': 10000,
        'num_students': 39,
        'num_lessons': 12,
        'min_students': 7,
        'max_students': 11,
    }
    print(
        f"\nСоздание курса '{csharp_params['title']}' с параметрами: \nстоимость - {csharp_params['cost']}, "
        f"\nчисло студентов - {csharp_params['num_students']}, \nчисло уроков - {csharp_params['num_lessons']}, "
        f"\nмин./макс. количество студентов в группе - {csharp_params['min_students']}/{csharp_params['max_students']}."
    )
    course_manager_csharp = CourseManager(**csharp_params)
    teacher_uuid_csharp, _ = course_manager_csharp.add_teacher(
        'Петр', 'Петров'
    )
    print(f'\nПреподаватель Петр Петров добавлен.')
    _ = course_manager_csharp.add_course(
        '2023-01-02T09:00:00Z', teacher_uuid_csharp
    )
    course_manager_csharp.add_lessons()
    print(f'\nУроки добавлены.')
    print(
        f'\nДобавляем студентов на курс по второму алгоритму: группа заполняется полностью, открывается следующая, студенты равномерно распределяются по группам, далее группы заполняются полностью и т.д.'
    )
    time.sleep(15)
    course_manager_csharp.add_students_to_course_evenly()

    print('\nВыводим распределение студентов по группам.')
    time.sleep(5)
    course_manager_csharp.print_course_details()

    print('\nСоздание курсов завершено.')
    time.sleep(3)

    k, v = list(course_manager_python.student_uuids.items())[0]
    print('\nПроверяем доступ пользователя к курсу Основы Python')
    course_manager_python.check_stdent_access(k, v)
    time.sleep(15)

    print('\nВыводим доступные для пользователя уроки по курсу Основы Python')
    time.sleep(5)
    print('-' * 60)
    course_manager_python.get_available_lessons(k)
    time.sleep(15)

    print('\nПроверяем доступ этого же пользователя к курсу Основы C#')
    course_manager_csharp.check_stdent_access(k, v)
    time.sleep(15)

    print('\nВыводим список курсов, доступных для заказа')
    time.sleep(5)
    print('-' * 60)
    course_manager_csharp.get_available_courses()
    time.sleep(5)

    print('\nВыводим стат. информацию о курсах')
    time.sleep(5)
    print('-' * 60)
    course_manager_csharp.print_courses_info()
    print('\nВсё! Благодарю за внимание!')


if __name__ == '__main__':
    main()
