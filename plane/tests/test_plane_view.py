from django.test import TestCase
from rest_framework.test import APIRequestFactory
from http import HTTPStatus
from .. import models
from common.action import ActionEnum
from .. import views


class TestPlaneView(TestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_list_without_content(self):
        view = views.PlaneViewSet.as_view({"get": ActionEnum.list.value})
        request = self.factory.get("/")
        response = view(request)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.data["count"], 0)
        self.assertEquals(len(response.data["results"]), 0)

    def test_list(self):
        models.Plane.objects.create(name="Hello world", description="Hello world")

        view = views.PlaneViewSet.as_view({"get": ActionEnum.list.value})
        request = self.factory.get("/")
        response = view(request)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.data["count"], 1)
        self.assertEquals(len(response.data["results"]), 1)

        result = dict(response.data["results"][0])
        self.assertEquals(result, {"name": "Hello world", "description": "Hello world"} | result)

    def test_retrieve(self):
        plane = models.Plane.objects.create(name="Hello world", description="Hello world")
        models.MaintenanceRecord.objects.create(plane=plane, name="Hello world", description="Hello world")
        models.MaintenanceRecord.objects.create(plane=plane, name="Hello world", description="Hello world")
        models.MaintenanceRecord.objects.create(plane=plane, name="Hello world", description="Hello world")

        view = views.PlaneViewSet.as_view({"get": ActionEnum.retrieve.value})
        request = self.factory.get(f"/")
        response = view(request, pk=plane.pk)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        result = dict(response.data)
        self.assertEquals(result, {"name": "Hello world", "description": "Hello world"} | result)
        self.assertEquals(len(result["records"]), 3)
