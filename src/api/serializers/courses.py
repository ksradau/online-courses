from rest_framework import serializers
from api.models import Course, Lecture, HomeWork, HomeWorkDone, Mark, Comment
from django.contrib.auth import get_user_model


User = get_user_model()


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['id', 'number', 'topic', 'presentation', 'course']


class LecturePutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['id', 'number', 'topic', 'presentation']


class RelatedUserSerializer(serializers.PrimaryKeyRelatedField, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class CourseSerializer(serializers.ModelSerializer):
    teachers = RelatedUserSerializer(many=True, required=False,
                                     queryset=User.objects.filter(groups__name='Teacher'))
    lecture = LectureSerializer(many=True, read_only=True)
    students = RelatedUserSerializer(many=True, required=False,
                                     queryset=User.objects.filter(groups__name='Student'))
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Course
        fields = ['id',
                  'title',
                  'students',
                  'teachers',
                  'lecture',
                  'creator',
                  ]


class HomeWorkSerializer(serializers.ModelSerializer):
    lecture = serializers.PrimaryKeyRelatedField(queryset=Lecture.objects.all())

    class Meta:
        model = HomeWork
        fields = ['id', 'task', 'description', 'lecture']


class HomeWorkDoneSerializer(serializers.ModelSerializer):
    homework = serializers.PrimaryKeyRelatedField(queryset=HomeWork.objects.all())
    student = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = HomeWorkDone
        fields = ['id', 'solution', 'homework', 'student']

    def validate(self, data):
        if HomeWorkDone.objects.filter(homework=data.get('homework'), student=self.context['request'].user):
            raise serializers.ValidationError("Sorry, you had already send your homework on this task.")
        return data


class MarkSerializer(serializers.ModelSerializer):
    homework_done = serializers.PrimaryKeyRelatedField(queryset=HomeWorkDone.objects.all())
    teacher = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Mark
        fields = ['id', 'value', 'homework_done', 'teacher']

    def validate(self, data):
        if Mark.objects.filter(homework_done=data.get('homework_done')):
            raise serializers.ValidationError(
                "You had already evaluate this homework. Make PUT request to change the mark.")
        return data


class MarkPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = ['id', 'value']


class CommentSerializer(serializers.ModelSerializer):
    mark = serializers.PrimaryKeyRelatedField(queryset=Mark.objects.all())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ['id', 'text', 'mark', 'user']
