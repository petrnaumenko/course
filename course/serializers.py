from rest_framework import serializers

from .models import Course, CourseTeacher, Lesson, Student, Teacher


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['teacher_uuid', 'first_name', 'last_name']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['student_uuid', 'first_name', 'last_name']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

    def create(self, validated_data):
        # Проверка наличия курса при добавлении урока
        course_id = validated_data.get('course').course_uuid
        if not Course.objects.filter(course_uuid=course_id).exists():
            raise serializers.ValidationError('Course not found.')
        return Lesson.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Запрет на изменение курса при обновлении урока
        if 'course' in validated_data:
            raise serializers.ValidationError(
                'You cannot change the course for an existing lesson.'
            )
        return super().update(instance, validated_data)


class CourseSerializer(serializers.ModelSerializer):
    teachers = serializers.ListField(
        child=serializers.UUIDField(), write_only=True, required=False
    )

    class Meta:
        model = Course
        fields = [
            'course_uuid',
            'title',
            'start_datetime',
            'cost',
            'min_students',
            'max_students',
            'teachers',
        ]

    def create(self, validated_data):
        teachers_uuids = validated_data.pop('teachers', [])
        course = Course.objects.create(**validated_data)
        self._create_course_teachers(course, teachers_uuids)
        return course

    def update(self, instance, validated_data):
        teachers_uuids = validated_data.pop('teachers', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if teachers_uuids is not None:
            instance.teachers.clear()
            self._create_course_teachers(instance, teachers_uuids)
        return instance

    def _create_course_teachers(self, course, teachers_uuids):
        for teacher_uuid in teachers_uuids:
            teacher = Teacher.objects.get(teacher_uuid=teacher_uuid)
            CourseTeacher.objects.create(course=course, teacher=teacher)
