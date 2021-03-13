from rest_framework import generics
from api.serializers.auth import UserCreateSerializer, UserLoginSerializer
from api.permissions import CoursePermission, LecturePermission, HomeWorkPermission, HomeWorkDonePermission, \
    MarkPermission, CommentPermission, IsNotAuthenticated
from rest_framework import permissions
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import views
from django.contrib.auth import authenticate, login, logout


User = get_user_model()


class RegisterView(generics.CreateAPIView):
    model = User
    permission_classes = [IsNotAuthenticated]
    serializer_class = UserCreateSerializer

    def get(self, request):
        return Response({"detail": "Here you can sign up."})


class LoginView(views.APIView):
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


class LogoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        logout(request)
        return Response({"detail": "You are logged out."})
