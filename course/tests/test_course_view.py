from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from common.action import ActionEnum
from course.models import Course
from course.views import CourseViewSet
from plane.models import Plane


class CourseViewTest(TestCase):
    def setUp(self) -> None:
        self.plane = Plane.objects.create(name="Test Plane")
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.factory = APIRequestFactory()

    def test_list_view(self):
        view = CourseViewSet.as_view({"get": ActionEnum.list.value})
        request = self.factory.get("/")
        force_authenticate(request, self.user)
        response = view(request)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.data["count"], 0)
        self.assertEquals(len(response.data["results"]), 0)

    def test_list_view_2(self):
        Course.objects.create(name="Test Course", description="Test Description")
        Course.objects.create(name="Test Course", description="Test Description")

        view = CourseViewSet.as_view({"get": ActionEnum.list.value})
        request = self.factory.get("/")
        force_authenticate(request, self.user)
        response = view(request)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.data["count"], 2)
        self.assertEquals(len(response.data["results"]), 2)

    def test_retrieve_view(self):
        course = Course.objects.create(name="Test Course", description="Test Description")
        view = CourseViewSet.as_view({"get": ActionEnum.retrieve.value})
        request = self.factory.get("/")
        force_authenticate(request, self.user)
        response = view(request, pk=course.pk)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.data["name"], "Test Course")
        self.assertEquals(response.data["description"], "Test Description")

    def test_create_view(self):
        view = CourseViewSet.as_view({"post": ActionEnum.create.value})
        request = self.factory.post("/", {"name": "Test Course", "description": "Test Description"})
        force_authenticate(request, self.user)
        response = view(request)
        self.assertEquals(response.status_code, HTTPStatus.CREATED)
        self.assertEquals(response.data["name"], "Test Course")
        self.assertEquals(response.data["description"], "Test Description")

    def test_update_view(self):
        course = Course.objects.create(name="Test Course", description="Test Description")
        view = CourseViewSet.as_view({"put": ActionEnum.update.value})
        request = self.factory.put("/", {"name": "Test Course", "description": "Test Description"})
        force_authenticate(request, self.user)
        response = view(request, pk=course.pk)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.data["name"], "Test Course")
        self.assertEquals(response.data["description"], "Test Description")
