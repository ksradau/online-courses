from rest_framework import viewsets as vs
from rest_framework import views as v
from rest_framework import generics as g
from rest_framework import mixins as m
from api.models import Course, Lecture, HomeWork, HomeWorkDone, Mark, Comment
from api.serializers import CourseSerializer, LectureSerializer, HomeWorkSerializer, HomeWorkDoneSerializer, \
    MarkSerializer, CommentSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth import get_user_model


class CourseViewSet(vs.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class LectureViewSet(vs.ModelViewSet):
    serializer_class = LectureSerializer
    queryset = Lecture.objects.all()


class HomeWorkViewSet(vs.ModelViewSet):
    serializer_class = HomeWorkSerializer
    queryset = HomeWork.objects.all()


class HomeWorkDoneViewSet(vs.ModelViewSet):
    serializer_class = HomeWorkDoneSerializer
    queryset = HomeWorkDone.objects.all()


class MarkViewSet(vs.ModelViewSet):
    serializer_class = MarkSerializer
    queryset = Mark.objects.all()


class CommentViewSet(vs.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class Register(APIView):
    def post(self, request):
        user = User.objects.create(
                username=request.data.get('username'),
                email=request.data.get('email'),
                first_name=request.data.get('firstName'),
                last_name=request.data.get('lastName')
            )
        user.set_password(str(request.data.get('password')))
        user.save()
        return Response({"status": "success", "response": "User Successfully Created"}, status=status.HTTP_201_CREATED)


class CreateUserView(g.CreateAPIView):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer
