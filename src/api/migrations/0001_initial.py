# Generated by Django 3.1.7 on 2021-03-08 22:33

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator', to=settings.AUTH_USER_MODEL)),
                ('students', models.ManyToManyField(related_name='course_students', to=settings.AUTH_USER_MODEL)),
                ('teachers', models.ManyToManyField(related_name='course_teachers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HomeWork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='HomeWorkDone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solution', models.TextField()),
                ('homework', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='homework_done', to='api.homework')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_homework_done', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(limit_value=1), django.core.validators.MaxValueValidator(limit_value=10)])),
                ('homework_done', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='mark', to='api.homeworkdone')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='teacher_mark', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField()),
                ('topic', models.CharField(max_length=255)),
                ('presentation', models.FileField(upload_to='presentations/')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lecture', to='api.course')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lecture_creator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='homework',
            name='lecture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homework', to='api.lecture'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('mark', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='api.mark')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_comment', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
