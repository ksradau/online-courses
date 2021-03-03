from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models as m
from django.contrib.auth.models import User


class Course(m.Model):
    user = m.ManyToManyField(User)
    title = m.CharField(max_length=100)

    def __str__(self):
        return f"Course '{ self.title }'"


class Lecture(m.Model):
    number = m.PositiveIntegerField()
    topic = m.CharField(max_length=255)
    presentation = m.FileField(upload_to='presentations/')
    course = m.ForeignKey(Course, on_delete=m.CASCADE, related_name="lecture")

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
    homework = m.OneToOneField(HomeWork, on_delete=m.CASCADE, related_name="homework_done")
    student = m.ForeignKey(User, on_delete=m.CASCADE, related_name="student_homework_done")

    def __str__(self):
        return f"Solution for the { self.homework }"


class Mark(m.Model):
    value = m.PositiveSmallIntegerField(validators=(MinValueValidator(limit_value=1),
                                                    MaxValueValidator(limit_value=10)))
    homework_done = m.OneToOneField(HomeWorkDone, on_delete=m.CASCADE, related_name="mark")
    teacher = m.ForeignKey(User, on_delete=m.PROTECT, related_name="teacher_mark")

    def __str__(self):
        return f"Mark: { self.value }"


class Comment(m.Model):
    text = m.TextField()
    mark = m.ForeignKey(Mark, on_delete=m.CASCADE, related_name="comment")
    teacher = m.ForeignKey(User, on_delete=m.PROTECT, related_name="teacher_comment")

    def __str__(self):
        return f"Comment for the { self.mark }"
