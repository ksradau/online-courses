from rest_framework import serializers as s
from rest_framework import fields as f
from api.models import Course, Lecture, HomeWork, HomeWorkDone, Mark, Comment
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model


User = get_user_model()


class GroupSerializer(s.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']
        extra_kwargs = {
            'name': {'validators': []},
        }


class UserCreateSerializer(s.ModelSerializer):
    group = s.PrimaryKeyRelatedField(queryset=Group.objects.all(), write_only=True)
    password = f.CharField(write_only=True)
    confirm_password = f.CharField(write_only=True)

    def validate(self, data):
        if not data.get('password') or not data.get('confirm_password'):
            raise s.ValidationError("Please enter a password and confirm it.")
        if data.get('password') != data.get('confirm_password'):
            raise s.ValidationError("Passwords don't match.")
        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
    )

        validated_data['group'].user_set.add(user)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'confirm_password', 'group']


class UserSerializer(s.ModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ['id',
                  'groups',
                  'username',
                  ]


class LectureSerializer(s.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['number', 'topic', 'presentation', 'course']


class CourseSerializer(s.ModelSerializer):
    creator = UserSerializer()
    students = UserSerializer(many=True)
    teachers = UserSerializer(many=True)
    lecture = LectureSerializer(many=True)

    class Meta:
        model = Course
        fields = ['id',
                  'title',
                  'creator',
                  'students',
                  'teachers',
                  'lecture',
                  ]


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
