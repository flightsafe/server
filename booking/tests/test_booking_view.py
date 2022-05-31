import datetime
from datetime import timedelta
from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIRequestFactory, force_authenticate

from booking import models as booking
from booking import views
from common.action import ActionEnum
from plane import models as plane


class TestBookingView(TestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.plane = plane.Plane.objects.create(title="Hello world", description="Hello world")
        self.user = User.objects.create(username="test_user")

    def test_list(self):
        booking.BookingRecord.objects.create(plane=self.plane, start_time=timezone.now(),
                                             end_time=timezone.now() + timedelta(days=1),
                                             user=self.user)
        booking.BookingRecord.objects.create(plane=self.plane, start_time=timezone.now() + timedelta(days=1),
                                             end_time=timezone.now() + timedelta(days=2), user=self.user)

        view = views.BookingViewSet.as_view({"get": ActionEnum.list.value})
        request = self.factory.get("/")
        force_authenticate(request, self.user)
        response = view(request)
        self.assertEquals(response.status_code, HTTPStatus.OK)

    def test_create(self):
        view = views.BookingViewSet.as_view({"post": ActionEnum.create.value})
        request = self.factory.post("/", data={
            "plane": self.plane.id,
            "start_time": timezone.now(),
            "end_time": timezone.now() + timedelta(days=1)
        }, format="json")
        force_authenticate(request, self.user)
        response = view(request)
        self.assertEquals(response.status_code, HTTPStatus.CREATED)
        self.assertEquals(booking.BookingRecord.objects.count(), 1)


class TestBookingViewWithQuery(TestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.plane = plane.Plane.objects.create(title="Hello world", description="Hello world")
        self.user = User.objects.create(username="test_user")
        first_time = datetime.datetime(year=2020, month=5, day=2)
        second_time = datetime.datetime(year=2020, month=6, day=1)
        third_time = datetime.datetime(year=2020, month=7, day=31)
        booking.BookingRecord.objects.create(plane=self.plane, start_time=first_time,
                                             end_time=first_time + timedelta(days=1),
                                             user=self.user)
        booking.BookingRecord.objects.create(plane=self.plane, start_time=second_time,
                                             end_time=second_time + timedelta(days=30),
                                             user=self.user)

        booking.BookingRecord.objects.create(plane=self.plane, start_time=third_time,
                                             end_time=third_time + timedelta(days=60),
                                             user=self.user)
        self.view = views.BookingViewSet.as_view({"get": ActionEnum.list.value})

    def test_list_1(self):
        request = self.factory.get("/", data={"time": "2020-06-01"})
        force_authenticate(request, self.user)
        response = self.view(request)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(len(response.data["results"]), 2)

    def test_list_2(self):
        request = self.factory.get("/", data={"time": "2020-06-10"})
        force_authenticate(request, self.user)
        response = self.view(request)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(len(response.data["results"]), 2)

    def test_list_3(self):
        request = self.factory.get("/", data={"time": "2020-07-10"})
        force_authenticate(request, self.user)
        response = self.view(request)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(len(response.data["results"]), 2)

    def test_list_4(self):
        request = self.factory.get("/", data={"time": "2020-05-10"})
        force_authenticate(request, self.user)
        response = self.view(request)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(len(response.data["results"]), 2)
