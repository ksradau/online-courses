from rest_framework import serializers as s
from api.models import Course, Lecture, HomeWork, HomeWorkDone, Mark, Comment
from django.contrib.auth.models import Group, User


class GroupSerializer(s.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']


class UserSerializer(s.ModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff', 'groups']


class CourseSerializer(s.ModelSerializer):
    # teachers = UserSerializer(many=True)
    # students = UserSerializer(many=True)

    class Meta:
        model = Course
        fields = ['title',
                  # 'teachers',
                  # 'students',
                  ]


class LectureSerializer(s.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['number', 'topic', 'presentation', 'course']


class HomeWorkSerializer(s.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['task', 'description', 'lecture']


class HomeWorkDoneSerializer(s.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['solution', 'homework', 'student']


class MarkSerializer(s.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['value', 'homework_done', 'teacher']


class CommentSerializer(s.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['text', 'mark', 'teacher']
