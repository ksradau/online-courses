from rest_framework import viewsets as vs
from rest_framework import generics as g
from api.models import Course, Lecture, HomeWork, HomeWorkDone, Mark, Comment
from api.serializers import CourseSerializer, LectureSerializer, HomeWorkSerializer, HomeWorkDoneSerializer, \
    MarkSerializer, CommentSerializer, UserCreateSerializer, LecturePutSerializer, MarkPutSerializer, \
    UserLoginSerializer
from api.permissions import CoursePermission, LecturePermission, HomeWorkPermission, HomeWorkDonePermission, \
    MarkPermission, CommentPermission, IsNotAuthenticated
from rest_framework import permissions as p
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import views as v
from django.contrib.auth import authenticate, login, logout


User = get_user_model()


class CourseViewSet(vs.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [p.IsAuthenticated, CoursePermission]

    def get_queryset(self):
        return Course.objects.filter(Q(creator=self.request.user)
                                     | Q(teachers=self.request.user)
                                     | Q(students=self.request.user)
                                     ).distinct()


class LectureViewSet(vs.ModelViewSet):
    serializer_class = LectureSerializer
    permission_classes = [p.IsAuthenticated, LecturePermission]

    def get_queryset(self):
        return Lecture.objects.filter(Q(course__creator=self.request.user)
                                     | Q(course__teachers=self.request.user)
                                     | Q(course__students=self.request.user)
                                     ).distinct()

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'PUT':
            serializer_class = LecturePutSerializer
        return serializer_class


class HomeWorkViewSet(vs.ModelViewSet):
    serializer_class = HomeWorkSerializer
    permission_classes = [p.IsAuthenticated, HomeWorkPermission]
    http_method_names = ['get', 'post', 'head', 'options', 'delete']

    def get_queryset(self):
        return HomeWork.objects.filter(Q(lecture__course__creator=self.request.user)
                                     | Q(lecture__creator=self.request.user)
                                     | Q(lecture__course__teachers=self.request.user)
                                     | Q(lecture__course__students=self.request.user)
                                     ).distinct()


class HomeWorkDoneViewSet(vs.ModelViewSet):
    serializer_class = HomeWorkDoneSerializer
    permission_classes = [p.IsAuthenticated, HomeWorkDonePermission]
    http_method_names = ['get', 'post', 'head', 'options']

    def get_queryset(self):
        return HomeWorkDone.objects.filter(Q(homework__lecture__creator=self.request.user)
                                     | Q(student=self.request.user)
                                     ).distinct()


class MarkViewSet(vs.ModelViewSet):
    serializer_class = MarkSerializer
    permission_classes = [p.IsAuthenticated, MarkPermission]
    http_method_names = ['get', 'post', 'head', 'options', 'put', 'patch']

    def get_queryset(self):
        return Mark.objects.filter(Q(homework_done__homework__lecture__creator=self.request.user) |
                                   Q(homework_done__student=self.request.user)).distinct()

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'PUT':
            serializer_class = MarkPutSerializer
        return serializer_class


class CommentViewSet(vs.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [p.IsAuthenticated, CommentPermission]
    http_method_names = ['get', 'post', 'head', 'options']

    def get_queryset(self):
        return Comment.objects.filter(Q(mark__teacher=self.request.user)
                                     | Q(mark__homework_done__student=self.request.user)
                                     ).distinct()


class RegisterView(g.CreateAPIView):
    model = User
    permission_classes = [IsNotAuthenticated]
    serializer_class = UserCreateSerializer

    def get(self, request):
        return Response({"detail": "Here you can sign up."})


class LoginView(v.APIView):
    model = User
    permission_classes = [IsNotAuthenticated]
    serializer_class = UserLoginSerializer

    def get(self, request):
        return Response({"detail": "Here you can log in."})

    def post(self, request):
        user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
        if user is not None:
            login(request, user)
            return Response({"detail": "You are logged in!"})
        return Response({"detail": "Error! Authentication was failed."})


class LogoutView(v.APIView):
    permission_classes = [p.IsAuthenticated]

    def get(self, request):
        logout(request)
        return Response({"detail": "You are logged out."})
