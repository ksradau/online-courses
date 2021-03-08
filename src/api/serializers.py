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
    class Meta:
        model = User
        fields = ['id', 'username']


class LectureSerializer(s.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['id', 'number', 'topic', 'presentation', 'course']


class LecturePutSerializer(s.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['id', 'number', 'topic', 'presentation']


class RelatedUserSerializer(s.PrimaryKeyRelatedField, s.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class CourseSerializer(s.ModelSerializer):
    teachers = RelatedUserSerializer(many=True, required=False,
                                     queryset=User.objects.filter(groups__name='Teacher'))
    lecture = LectureSerializer(many=True, read_only=True)
    students = RelatedUserSerializer(many=True, required=False,
                                     queryset=User.objects.filter(groups__name='Student'))
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ['id',
                  'title',
                  'students',
                  'teachers',
                  'lecture',
                  'creator',
                  ]


class HomeWorkSerializer(s.ModelSerializer):
    lecture = s.PrimaryKeyRelatedField(queryset=Lecture.objects.all())

    class Meta:
        model = HomeWork
        fields = ['id', 'task', 'description', 'lecture']


class HomeWorkDoneSerializer(s.ModelSerializer):
    homework = s.PrimaryKeyRelatedField(queryset=HomeWork.objects.all())

    class Meta:
        model = HomeWorkDone
        fields = ['id', 'solution', 'homework']

    def validate(self, data):
        if HomeWorkDone.objects.filter(homework=data.get('homework'), student=self.context['request'].user):
            raise s.ValidationError("Sorry, you had already send your homework on this task.")
        return data


class MarkSerializer(s.ModelSerializer):
    homework_done = s.PrimaryKeyRelatedField(queryset=HomeWorkDone.objects.all())

    class Meta:
        model = Mark
        fields = ['id', 'value', 'homework_done']

    def validate(self, data):
        if Mark.objects.filter(homework_done=data.get('homework_done')):
            raise s.ValidationError("You had already evaluate this homework. Make PUT request to change the mark.")
        return data


class MarkPutSerializer(s.ModelSerializer):
    class Meta:
        model = Mark
        fields = ['id', 'value']


class CommentSerializer(s.ModelSerializer):
    mark = MarkSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'mark']
