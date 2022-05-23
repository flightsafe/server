from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from django.core import exceptions

from common.constants import BookingStatus
from plane import models as plane
from booking import models as booking
from datetime import timedelta


class TestBookingRecord(TestCase):
    def setUp(self) -> None:
        self.plane_1 = plane.Plane.objects.create(name="plane_1")
        self.plane_2 = plane.Plane.objects.create(name="plane_2")
        self.user = User.objects.create(username="mock_user")
        self.now = timezone.now()

    def test_booking_in_use_status(self):
        booking.BookingRecord.objects.create(plane=self.plane_1, start_time=self.now - timedelta(days=1),
                                             end_time=self.now + timedelta(days=1), user=self.user)
        self.assertEqual(self.plane_1.booking_status, BookingStatus.in_use.value)

    def test_booking_in_use_status_2(self):
        booking.BookingRecord.objects.create(plane=self.plane_1, start_time=self.now,
                                             end_time=self.now + timedelta(days=1), user=self.user)
        self.assertEqual(self.plane_1.booking_status, BookingStatus.in_use.value)

    def test_booking_not_in_use_status(self):
        booking.BookingRecord.objects.create(plane=self.plane_1, start_time=self.now + timedelta(days=1),
                                             end_time=self.now + timedelta(days=2), user=self.user)
        self.assertEqual(self.plane_1.booking_status, BookingStatus.not_in_use.value)

    def test_booking_not_in_use_status_2(self):
        booking.BookingRecord.objects.create(plane=self.plane_1, start_time=self.now - timedelta(days=2),
                                             end_time=self.now - timedelta(days=1), user=self.user)
        self.assertEqual(self.plane_1.booking_status, BookingStatus.not_in_use.value)

    def test_save(self):
        with self.assertRaises(expected_exception=exceptions.ValidationError):
            booking.BookingRecord.objects.create(plane=self.plane_1, start_time=self.now - timedelta(days=1),
                                                 end_time=self.now - timedelta(days=2), user=self.user)

        booking.BookingRecord.objects.create(plane=self.plane_1, start_time=self.now - timedelta(days=2),
                                             end_time=self.now + timedelta(days=2), user=self.user)

        with self.assertRaises(expected_exception=exceptions.ValidationError):
            booking.BookingRecord.objects.create(plane=self.plane_1, start_time=self.now - timedelta(days=1),
                                                 end_time=self.now, user=self.user)

        with self.assertRaises(expected_exception=exceptions.ValidationError):
            booking.BookingRecord.objects.create(plane=self.plane_1, start_time=self.now - timedelta(days=0),
                                                 end_time=self.now + timedelta(days=1), user=self.user)

        self.assertEqual(booking.BookingRecord.objects.count(), 1)