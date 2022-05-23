from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from booking.apps import BookingConfig
from booking.models import BookingRecord
from common.action import ActionEnum
from transaction.models import TransactionInfo, TransactionDetail, TransactionName
from transaction.views import TransactionViewSet


class TransactionViewTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.factory = APIRequestFactory()

    def test_list_view(self):
        view = TransactionViewSet.as_view({"get": ActionEnum.list.value})
        request = self.factory.get("/")
        force_authenticate(request, self.user)
        response = view(request)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.data["count"], 0)
        self.assertEquals(len(response.data["results"]), 0)

    def test_list_view_2(self):
        TransactionInfo.objects.create(name=TransactionName.create_lesson_record)
        TransactionInfo.objects.create(name=TransactionName.create_lesson_record)
        view = TransactionViewSet.as_view({"get": ActionEnum.list.value})
        request = self.factory.get("/")
        force_authenticate(request, self.user)
        response = view(request)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.data["count"], 2)
        self.assertEquals(len(response.data["results"]), 2)

    def test_list_view_3(self):
        details = TransactionDetail(app_label=BookingConfig.name,
                                    model_name=BookingRecord.__name__,
                                    pk=1)

        TransactionInfo.objects.create(name=TransactionName.create_lesson_record, details=details)
        TransactionInfo.objects.create(name=TransactionName.create_lesson_record, details=details)
        view = TransactionViewSet.as_view({"get": ActionEnum.list.value})
        request = self.factory.get("/")
        force_authenticate(request, self.user)
        response = view(request)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.data["count"], 2)
        self.assertEquals(len(response.data["results"]), 2)

    def test_create_view(self):
        view = TransactionViewSet.as_view({"post": ActionEnum.create.value})
        request = self.factory.post("/", {"name": TransactionName.create_lesson_record})
        force_authenticate(request, self.user)
        response = view(request)
        self.assertEquals(response.status_code, HTTPStatus.CREATED)
        self.assertEquals(response.data["name"], TransactionName.create_lesson_record.value)
        self.assertEquals(response.data["details"], None)

    def test_update_view(self):
        details = TransactionDetail(app_label=BookingConfig.name,
                                    model_name=BookingRecord.__name__,
                                    pk=1)
        info = TransactionInfo.objects.create(name=TransactionName.create_lesson_record, details=details)
        view = TransactionViewSet.as_view({"patch": ActionEnum.update.value})
        request = self.factory.patch("/", {"name": TransactionName.create_lesson_record, "details": details.to_dict()},
                                     format="json")
        force_authenticate(request, self.user)
        response = view(request, pk=info.pk)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.data["name"], TransactionName.create_lesson_record.value)
        self.assertEquals(response.data["details"], details.to_dict())

    def test_delete_view(self):
        details = TransactionDetail(app_label=BookingConfig.name,
                                    model_name=BookingRecord.__name__,
                                    pk=1)
        info = TransactionInfo.objects.create(name=TransactionName.create_lesson_record, details=details)
        view = TransactionViewSet.as_view({"delete": ActionEnum.delete.value})
        request = self.factory.delete("/", {"name": TransactionName.create_lesson_record, "details": details.to_dict()},
                                      format="json")
        force_authenticate(request, self.user)
        response = view(request, pk=info.pk)
        self.assertEquals(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEquals(TransactionInfo.objects.count(), 0)
        