from rest_framework import permissions as p
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from api.models import Course, Lecture, HomeWork, HomeWorkDone, Mark, Comment


User = get_user_model()


class CoursePermission(p.BasePermission):
    message = 'This request is permitted.'

    def has_permission(self, request, view):
        if request.method in p.SAFE_METHODS:
            return True
        return is_teacher(request.user)

    def has_object_permission(self, request, view, obj):
        if request.method in p.SAFE_METHODS:
            return True

        return obj.creator == request.user


class LecturePermission(p.BasePermission):
    message = 'This request is permitted.'

    def has_permission(self, request, view):
        if request.method in p.SAFE_METHODS:
            return True
        elif request.method == "POST":
            try:
                course = Course.objects.filter(id=request.data.get('course')).first()
                return is_teacher(request.user) and \
                        course.creator == request.user or request.user in course.teachers.all()
            except AttributeError:
                return True
        else:
            return is_teacher(request.user)

    def has_object_permission(self, request, view, obj):
        if request.method in p.SAFE_METHODS:
            return True
        return obj.creator == request.user


class HomeWorkPermission(p.BasePermission):
    message = 'This request is permitted.'

    def has_permission(self, request, view):
        if request.method in p.SAFE_METHODS:
            return True
        elif request.method == "POST":
            try:
                lecture = Lecture.objects.filter(id=request.data.get('lecture')).first()
                return is_teacher(request.user) and \
                  lecture.creator == request.user
            except AttributeError:
                return True
        else:
            return is_teacher(request.user)

    def has_object_permission(self, request, view, obj):
        if request.method in p.SAFE_METHODS:
            return True
        return obj.lecture.creator == request.user


class HomeWorkDonePermission(p.BasePermission):
    message = 'This request is permitted.'

    def has_permission(self, request, view):
        if request.method in p.SAFE_METHODS:
            return True
        elif request.method == "POST":
            try:
                homework = HomeWork.objects.filter(id=request.data.get('homework')).first()
                return is_student(request.user) and \
                  request.user in homework.lecture.course.students.all()
            except AttributeError:
                return True
        else:
            return is_student(request.user)


class MarkPermission(p.BasePermission):
    message = 'This request is permitted.'

    def has_permission(self, request, view):
        if request.method in p.SAFE_METHODS:
            return True
        elif request.method == "POST":
            try:
                homework_done = HomeWorkDone.objects.filter(id=request.data.get('homework_done')).first()
                return is_teacher(request.user) and homework_done.homework.lecture.creator == request.user
            except AttributeError:
                return True
        else:
            return is_teacher(request.user)

    def has_object_permission(self, request, view, obj):
        if request.method in p.SAFE_METHODS:
            return True
        return obj.homework_done.homework.lecture.creator == request.user


class CommentPermission(p.BasePermission):
    message = 'This request is permitted.'

    def has_permission(self, request, view):
        if request.method in p.SAFE_METHODS:
            return True
        elif request.method == "POST":
            try:
                mark = Mark.objects.filter(id=request.data.get('mark')).first()
                return (is_student(request.user) and mark.homework_done.student == request.user) or \
                       (is_teacher(request.user) and mark.teacher == request.user)
            except AttributeError:
                return True
        else:
            return True


def is_student(user):
    return user.groups.filter(name='Student').exists()


def is_teacher(user):
    return user.groups.filter(name='Teacher').exists()
