from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model
from storages.backends.s3boto3 import S3Boto3Storage


User = get_user_model()


class Course(models.Model):
    title = models.CharField(max_length=100)
    teachers = models.ManyToManyField(User, related_name="course_teachers")
    students = models.ManyToManyField(User, related_name="course_students")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")

    def __str__(self):
        return f"Course '{ self.title }'"


class Lecture(models.Model):
    number = models.PositiveIntegerField()
    topic = models.CharField(max_length=255)
    presentation = models.FileField(storage=S3Boto3Storage())
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lecture")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lecture_creator")

    def __str__(self):
        return f"Lecture №{ self.number } - '{ self.topic }'"


class HomeWork(models.Model):
    task = models.CharField(max_length=255)
    description = models.TextField()
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name="homework")

    def __str__(self):
        return f"Task '{ self.task }'"


class HomeWorkDone(models.Model):
    solution = models.TextField()
    homework = models.ForeignKey(HomeWork, on_delete=models.DO_NOTHING, related_name="homework_done")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student_homework_done")

    def __str__(self):
        return f"Solution for the { self.homework } by { self.student }"


class Mark(models.Model):
    value = models.PositiveSmallIntegerField(validators=(MinValueValidator(limit_value=1),
                                                         MaxValueValidator(limit_value=10)))
    homework_done = models.OneToOneField(HomeWorkDone, on_delete=models.CASCADE, related_name="mark")
    teacher = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="teacher_mark")

    def __str__(self):
        return f"Mark: { self.value }"


class Comment(models.Model):
    text = models.TextField()
    mark = models.ForeignKey(Mark, on_delete=models.CASCADE, related_name="comment")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="user_comment")

    def __str__(self):
        return f"Comment for the { self.mark }"


User.add_to_class("__str__", lambda self: f'{self.groups.first()}: {self.username}')
