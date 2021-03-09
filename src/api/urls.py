from rest_framework.routers import DefaultRouter
from django.urls import path, include, re_path
from api import views as v
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
router.register('courses', v.CourseViewSet, basename='courses')
router.register('lecture', v.LectureViewSet, basename='lecture')
router.register('homework', v.HomeWorkViewSet, basename='homework')
router.register('homework_done', v.HomeWorkDoneViewSet, basename='homework_done')
router.register('mark', v.MarkViewSet, basename='mark')
router.register('comment', v.CommentViewSet, basename='comment')

urlpatterns = [
    path(r'', include(router.urls)),
    path('sign-up/', v.RegisterView.as_view(), name='signup'),
    path("login/", v.LoginView.as_view(), name="login"),
    path("logout/", v.LogoutView.as_view(), name="logout"),
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
