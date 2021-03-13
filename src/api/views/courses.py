from rest_framework.viewsets import ModelViewSet
from api.models import Course, Lecture, HomeWork, HomeWorkDone, Mark, Comment
from api.serializers.courses import CourseSerializer, LectureSerializer, HomeWorkSerializer, HomeWorkDoneSerializer, \
    MarkSerializer, CommentSerializer, LecturePutSerializer, MarkPutSerializer
from api.permissions import CoursePermission, LecturePermission, HomeWorkPermission, HomeWorkDonePermission, \
    MarkPermission, CommentPermission, IsNotAuthenticated
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.db.models import Q


User = get_user_model()


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, CoursePermission]

    def get_queryset(self):
        return Course.objects.filter(Q(creator=self.request.user) |
                                     Q(teachers=self.request.user) |
                                     Q(students=self.request.user)
                                     ).distinct()


class LectureViewSet(ModelViewSet):
    serializer_class = LectureSerializer
    permission_classes = [IsAuthenticated, LecturePermission]

    def get_queryset(self):
        return Lecture.objects.filter(Q(course__creator=self.request.user) |
                                      Q(course__teachers=self.request.user) |
                                      Q(course__students=self.request.user)
                                      ).distinct()

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'PUT':
            serializer_class = LecturePutSerializer
        return serializer_class


class HomeWorkViewSet(ModelViewSet):
    serializer_class = HomeWorkSerializer
    permission_classes = [IsAuthenticated, HomeWorkPermission]
    http_method_names = ['get', 'post', 'head', 'options', 'delete']

    def get_queryset(self):
        return HomeWork.objects.filter(Q(lecture__course__creator=self.request.user) |
                                       Q(lecture__creator=self.request.user) |
                                       Q(lecture__course__teachers=self.request.user) |
                                       Q(lecture__course__students=self.request.user)
                                       ).distinct()


class HomeWorkDoneViewSet(ModelViewSet):
    serializer_class = HomeWorkDoneSerializer
    permission_classes = [IsAuthenticated, HomeWorkDonePermission]
    http_method_names = ['get', 'post', 'head', 'options']

    def get_queryset(self):
        return HomeWorkDone.objects.filter(Q(homework__lecture__creator=self.request.user)
                                     | Q(student=self.request.user)
                                     ).distinct()


class MarkViewSet(ModelViewSet):
    serializer_class = MarkSerializer
    permission_classes = [IsAuthenticated, MarkPermission]
    http_method_names = ['get', 'post', 'head', 'options', 'put', 'patch']

    def get_queryset(self):
        return Mark.objects.filter(Q(homework_done__homework__lecture__creator=self.request.user) |
                                   Q(homework_done__student=self.request.user)).distinct()

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'PUT':
            serializer_class = MarkPutSerializer
        return serializer_class


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, CommentPermission]
    http_method_names = ['get', 'post', 'head', 'options']

    def get_queryset(self):
        return Comment.objects.filter(Q(mark__teacher=self.request.user) |
                                      Q(mark__homework_done__student=self.request.user)).distinct()

