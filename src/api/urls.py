from rest_framework.routers import DefaultRouter
from django.urls import path, include, re_path
from api.views import CourseViewSet
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
router.register('course', CourseViewSet, basename='course')

urlpatterns = [
    path(r'', include(router.urls)),
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
