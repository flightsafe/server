from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions

from course.models import Course, Comment, Lesson, LessonHistory
from course.serializers import CourseSerializer, CommentSerializer, LessonSerializer, LessonHistorySerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.order_by("id").all()
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.order_by("id").all()
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]

    def create(self, request, *args, **kwargs):
        request.data["author"] = request.user.pk
        return super().create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.order_by("id").all()
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = LessonSerializer
    filter_backends = [DjangoFilterBackend]


class LessonHistoryViewSet(viewsets.ModelViewSet):
    queryset = LessonHistory.objects.order_by("id").all()
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = LessonHistorySerializer
    filter_backends = [DjangoFilterBackend]

    def create(self, request, *args, **kwargs):
        request.data["student"] = request.user.pk
        return super().create(request, *args, **kwargs)



