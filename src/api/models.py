from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models as m
from django.contrib.auth import get_user_model


User = get_user_model()


class Course(m.Model):
    title = m.CharField(max_length=100)
    teachers = m.ManyToManyField(User, related_name="course_teachers")
    students = m.ManyToManyField(User, related_name="course_students")
    creator = m.ForeignKey(User, on_delete=m.DO_NOTHING, related_name="creator")

    def __str__(self):
        return f"Course '{ self.title }'"


class Lecture(m.Model):
    number = m.PositiveIntegerField()
    topic = m.CharField(max_length=255)
    presentation = m.FileField(upload_to='presentations/')
    course = m.ForeignKey(Course, on_delete=m.CASCADE, related_name="lecture")
    creator = m.ForeignKey(User, on_delete=m.DO_NOTHING, related_name="lecture_creator")

    def __str__(self):
        return f"Lecture №{ self.number } - '{ self.topic }'"


class HomeWork(m.Model):
    task = m.CharField(max_length=255)
    description = m.TextField()
    lecture = m.ForeignKey(Lecture, on_delete=m.CASCADE, related_name="homework")

    def __str__(self):
        return f"Task '{ self.task }'"


class HomeWorkDone(m.Model):
    solution = m.TextField()
    homework = m.ForeignKey(HomeWork, on_delete=m.CASCADE, related_name="homework_done")
    student = m.ForeignKey(User, on_delete=m.CASCADE, related_name="student_homework_done")

    def __str__(self):
        return f"Solution for the { self.homework }"


class Mark(m.Model):
    value = m.PositiveSmallIntegerField(validators=(MinValueValidator(limit_value=1),
                                                    MaxValueValidator(limit_value=10)))
    homework_done = m.OneToOneField(HomeWorkDone, on_delete=m.CASCADE, related_name="mark")
    teacher = m.ForeignKey(User, on_delete=m.DO_NOTHING, related_name="teacher_mark")

    def __str__(self):
        return f"Mark: { self.value }"


class Comment(m.Model):
    text = m.TextField()
    mark = m.ForeignKey(Mark, on_delete=m.CASCADE, related_name="comment")
    user = m.ForeignKey(User, on_delete=m.DO_NOTHING, related_name="user_comment")

    def __str__(self):
        return f"Comment for the { self.mark }"


User.add_to_class("__str__", lambda self: f'{self.groups.first()} {self.first_name} {self.last_name}')
