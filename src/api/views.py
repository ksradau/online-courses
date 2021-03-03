from rest_framework import viewsets as v
from rest_framework import mixins as m
from api.models import Course, Lecture, HomeWork, HomeWorkDone, Mark, Comment
from api.serializers import CourseSerializer, LectureSerializer, HomeWorkSerializer, HomeWorkDoneSerializer, \
    MarkSerializer, CommentSerializer


class CourseViewSet(v.GenericViewSet, m.ListModelMixin, m.CreateModelMixin, m.RetrieveModelMixin,
                    m.UpdateModelMixin, m.DestroyModelMixin):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
