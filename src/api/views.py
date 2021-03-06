from rest_framework import viewsets as vs
from rest_framework import views as v
from rest_framework import generics as g
from rest_framework import mixins as m
from api.models import Course, Lecture, HomeWork, HomeWorkDone, Mark, Comment
from api.serializers import CourseSerializer, LectureSerializer, HomeWorkSerializer, HomeWorkDoneSerializer, \
    MarkSerializer, CommentSerializer, UserCreateSerializer
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Q


User = get_user_model()


class CourseViewSet(vs.ModelViewSet):
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        return Course.objects.filter(Q(creator=self.request.user)
                                     | Q(teachers=self.request.user)
                                     | Q(students=self.request.user)
                                     ).distinct()


class LectureViewSet(vs.ModelViewSet):
    serializer_class = LectureSerializer
    queryset = Lecture.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class HomeWorkViewSet(vs.ModelViewSet):
    serializer_class = HomeWorkSerializer
    queryset = HomeWork.objects.all()


class HomeWorkDoneViewSet(vs.ModelViewSet):
    serializer_class = HomeWorkDoneSerializer
    queryset = HomeWorkDone.objects.all()

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class MarkViewSet(vs.ModelViewSet):
    serializer_class = MarkSerializer
    queryset = Mark.objects.all()

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class CommentViewSet(vs.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CreateUserView(g.CreateAPIView):
    model = User
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserCreateSerializer
