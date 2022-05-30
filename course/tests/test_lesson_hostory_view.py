from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from common.action import ActionEnum
from course.models import Course, Lesson, LessonHistory
from course.views import LessonHistoryViewSet
from plane.models import Plane


class LessonHistoryTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(title="Test Course", description="Test Description")
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.factory = APIRequestFactory()
        self.lesson = Lesson.objects.create(title="Test Lesson", description="Test Description", course=self.course)
        self.plane = Plane.objects.create(title="plane")

    def test_list_view(self):
        view = LessonHistoryViewSet.as_view({"get": ActionEnum.list.value})
        request = self.factory.get("/")
        force_authenticate(request, self.user)
        response = view(request)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.data["count"], 0)
        self.assertEquals(len(response.data["results"]), 0)

    def test_list_view_2(self):
        LessonHistory.objects.create(lesson=self.lesson, student=self.user, plane=self.plane)
        LessonHistory.objects.create(lesson=self.lesson, student=self.user, plane=self.plane)
        view = LessonHistoryViewSet.as_view({"get": ActionEnum.list.value})
        request = self.factory.get("/")
        force_authenticate(request, self.user)
        response = view(request)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.data["count"], 2)
        self.assertEquals(len(response.data["results"]), 2)

    def test_retrieve_view(self):
        lesson_history = LessonHistory.objects.create(lesson=self.lesson, student=self.user, plane=self.plane)
        view = LessonHistoryViewSet.as_view({"get": ActionEnum.retrieve.value})
        request = self.factory.get("/")
        force_authenticate(request, self.user)
        response = view(request, pk=lesson_history.pk)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.data["lesson"], self.lesson.pk)
        self.assertEquals(response.data["student"], self.user.pk)
        self.assertEquals(response.data["plane"], self.plane.pk)

    def test_create_view(self):
        view = LessonHistoryViewSet.as_view({"post": ActionEnum.create.value})
        request = self.factory.post("/", {"lesson": self.lesson.pk, "student": self.user.pk, "plane": self.plane.pk},
                                    format="json")
        force_authenticate(request, self.user)
        response = view(request)
        self.assertEquals(response.status_code, HTTPStatus.CREATED)
        self.assertEquals(response.data["lesson"], self.lesson.pk)
        self.assertEquals(response.data["student"], self.user.pk)
        self.assertEquals(response.data["plane"], self.plane.pk)

    def test_update_view(self):
        lesson_history = LessonHistory.objects.create(lesson=self.lesson, student=self.user, plane=self.plane)
        view = LessonHistoryViewSet.as_view({"patch": ActionEnum.update.value})
        request = self.factory.patch("/")
        force_authenticate(request, self.user)
        response = view(request, pk=lesson_history.pk)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.data["lesson"], self.lesson.pk)
        self.assertEquals(response.data["student"], self.user.pk)
        self.assertEquals(response.data["plane"], self.plane.pk)

    def test_delete_view(self):
        lesson_history = LessonHistory.objects.create(lesson=self.lesson, student=self.user, plane=self.plane)
        view = LessonHistoryViewSet.as_view({"delete": ActionEnum.delete.value})
        request = self.factory.delete("/")
        force_authenticate(request, self.user)
        response = view(request, pk=lesson_history.pk)
        self.assertEquals(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEquals(LessonHistory.objects.count(), 0)
