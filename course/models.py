import uuid

from django.db import models


# Модель Преподавателя
class Teacher(models.Model):
    teacher_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


# Модель Курса
class Course(models.Model):
    course_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=200)
    start_datetime = models.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    min_students = models.IntegerField()
    max_students = models.IntegerField()
    teachers = models.ManyToManyField(Teacher, through='CourseTeacher')

    def __str__(self):
        return self.title


# Кросс-таблица Преподаватель - Курс
class CourseTeacher(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


# Модель Урока
class Lesson(models.Model):
    lesson_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    materials = models.TextField()

    def __str__(self):
        return self.title


# Модель Студента
class Student(models.Model):
    student_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


# Модель Группы
class Group(models.Model):
    group_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    students = models.ManyToManyField('Student', through='StudentGroup')

    def __str__(self):
        return self.name


# Кросс-таблица Студент - Группа
class StudentGroup(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
