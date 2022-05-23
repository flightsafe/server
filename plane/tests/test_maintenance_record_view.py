from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from common.action import ActionEnum
from plane import views, models


class TestMaintenanceRecordView(TestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.plane = models.Plane.objects.create(name="Hello world", description="Hello world")
        self.user = User.objects.create(username="test_user")

    def test_list_without_content(self):
        view = views.MaintenanceViewSet.as_view({"get": ActionEnum.list.value})
        request = self.factory.get("/")
        force_authenticate(request, self.user)
        response = view(request)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.data["count"], 0)
        self.assertEquals(len(response.data["results"]), 0)

    def test_list(self):
        models.MaintenanceRecord.objects.create(plane=self.plane, name="Hello world", description="Hello world",
                                                author=self.user)

        view = views.MaintenanceViewSet.as_view({"get": ActionEnum.list.value})
        request = self.factory.get("/")
        force_authenticate(request, self.user)
        response = view(request)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.data["count"], 1)
        self.assertEquals(len(response.data["results"]), 1)

        result = dict(response.data["results"][0])
        self.assertEquals(result, {"name": "Hello world", "description": "Hello world"} | result)

    def test_retrieve(self):
        record = models.MaintenanceRecord.objects.create(plane=self.plane, name="Hello world",
                                                         description="Hello world", author=self.user)
        models.MaintenanceRecordItem.objects.create(name="Hello world", description="Hello world",
                                                    maintenance_record=record, operator=self.user)
        models.MaintenanceRecordItem.objects.create(name="Hello world", description="Hello world",
                                                    maintenance_record=record, operator=self.user)
        models.MaintenanceRecordItem.objects.create(name="Hello world", description="Hello world",
                                                    maintenance_record=record, operator=self.user)

        view = views.MaintenanceViewSet.as_view({"get": ActionEnum.retrieve.value})
        request = self.factory.get(f"/")
        force_authenticate(request, self.user)
        response = view(request, pk=record.pk)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        result = dict(response.data)
        self.assertEquals(result, {"name": "Hello world", "description": "Hello world"} | result)
        self.assertEquals(len(result["items"]), 3)
