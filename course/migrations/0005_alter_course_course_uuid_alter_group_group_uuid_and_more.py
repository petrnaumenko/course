# Generated by Django 5.0.2 on 2024-02-29 18:16

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_rename_uuid_course_course_uuid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_uuid',
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name='group',
            name='group_uuid',
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='lesson_uuid',
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_uuid',
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='teacher_uuid',
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
    ]