from rest_framework.routers import DefaultRouter
from django.urls import path, include, re_path
from api.views import courses, auth
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import IsAuthenticated


schema_view = get_schema_view(
    openapi.Info(
        title="Online Courses Platform API",
        default_version="v1",
        description="API for Online Courses Platform",
        contact=openapi.Contact(email="sushei.ekaterina@gmail.com"),
    ),
    public=True,
    permission_classes=(IsAuthenticated,),
)

router = DefaultRouter()
router.register('courses', courses.CourseViewSet, basename='courses')
router.register('lecture', courses.LectureViewSet, basename='lecture')
router.register('homework', courses.HomeWorkViewSet, basename='homework')
router.register('homework_done', courses.HomeWorkDoneViewSet, basename='homework_done')
router.register('mark', courses.MarkViewSet, basename='mark')
router.register('comment', courses.CommentViewSet, basename='comment')

urlpatterns = [
    path(r'', include(router.urls)),
    path('sign-up/', auth.RegisterView.as_view(), name='signup'),
    path("login/", auth.LoginView.as_view(), name="login"),
    path("logout/", auth.LogoutView.as_view(), name="logout"),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
