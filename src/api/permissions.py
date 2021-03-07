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
    pass


class HomeWorkDonePermission(p.BasePermission):
    pass


class MarkPermission(p.BasePermission):
    pass


class CommentPermission(p.BasePermission):
    pass


def is_student(user):
    return user.groups.filter(name='Student').exists()


def is_teacher(user):
    return user.groups.filter(name='Teacher').exists()
