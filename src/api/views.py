from rest_framework import viewsets as v
from rest_framework import mixins as m
from api.models import Course, Lecture, HomeWork, HomeWorkDone, Mark, Comment
from api.serializers import CourseSerializer, LectureSerializer, HomeWorkSerializer, HomeWorkDoneSerializer, \
    MarkSerializer, CommentSerializer


class CourseViewSet(v.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class LectureViewSet(v.ModelViewSet):
    serializer_class = LectureSerializer
    queryset = Lecture.objects.all()


class HomeWorkViewSet(v.ModelViewSet):
    serializer_class = HomeWorkSerializer
    queryset = HomeWork.objects.all()


class HomeWorkDoneViewSet(v.ModelViewSet):
    serializer_class = HomeWorkDoneSerializer
    queryset = HomeWorkDone.objects.all()


class MarkViewSet(v.ModelViewSet):
    serializer_class = MarkSerializer
    queryset = Mark.objects.all()


class CommentViewSet(v.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
