from django.urls import path, include
from rest_framework import routers

from course import views

router = routers.DefaultRouter()
router.register(r"course", views.CourseViewSet, basename="course")
router.register(r"comment", views.CommentViewSet, basename="comment")
router.register(r"lesson", views.LessonViewSet, basename="lesson")
router.register(r"lessonhistory", views.LessonHistoryViewSet, basename="lesson-history")

urlpatterns = [
    path("", include(router.urls))
]
