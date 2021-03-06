from django.contrib import admin
from api.models import Course, Lecture, HomeWork, HomeWorkDone, Mark, Comment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    pass


@admin.register(HomeWork)
class HomeWorkAdmin(admin.ModelAdmin):
    pass


@admin.register(HomeWorkDone)
class HomeWorkDoneAdmin(admin.ModelAdmin):
    pass


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
