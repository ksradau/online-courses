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
        fields = ['first_name', 'last_name', 'groups']


class CourseSerializer(s.ModelSerializer):
    user = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id',
                  'title',
                  'user',
                  ]


class LectureSerializer(s.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['number', 'topic', 'presentation', 'course']


class HomeWorkSerializer(s.ModelSerializer):
    class Meta:
        model = HomeWork
        fields = ['task', 'description', 'lecture']


class HomeWorkDoneSerializer(s.ModelSerializer):
    class Meta:
        model = HomeWorkDone
        fields = ['solution', 'homework', 'student']


class MarkSerializer(s.ModelSerializer):
    class Meta:
        model = Mark
        fields = ['value', 'homework_done', 'teacher']


class CommentSerializer(s.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text', 'mark', 'teacher']
