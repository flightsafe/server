from datetime import timedelta

from django.contrib.auth.models import User
from django.core import exceptions
from django.test import TestCase
from django.utils import timezone

from plane.models import Plane
from transaction.models import TransactionInfo, TransactionName, TransactionDetail
from booking.models import BookingRecord
from booking.apps import BookingConfig


class TestTransactionInfo(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="user")
        self.now = timezone.now()
        self.plane = Plane.objects.create(name="plane")

    def test_add_transaction(self):
        details = TransactionDetail(app_label=BookingConfig.name,
                                    model_name=BookingRecord.__name__,
                                    pk=1)
        tx = TransactionInfo.objects.create(name=TransactionName.create_booking,
                                            details=details,
                                            user=self.user)

        self.assertEquals(tx.details, details)

    def test_add_transaction_2(self):
        details = TransactionDetail(app_label=BookingConfig.name,
                                    model_name=BookingRecord.__name__,
                                    pk=1)
        tx = TransactionInfo.objects.create(name=TransactionName.create_booking,
                                            details=details)

        self.assertEquals(tx.details, details)

    def test_add_transaction_error(self):
        with self.assertRaises(expected_exception=exceptions.ValidationError):
            details = TransactionDetail(app_label="invalid_app_label",
                                        model_name=BookingRecord.__name__,
                                        pk=1)
            tx = TransactionInfo.objects.create(name=TransactionName.create_booking,
                                                details=details,
                                                user=self.user)

    def test_add_transaction_error_2(self):
        with self.assertRaises(expected_exception=exceptions.ValidationError):
            details = TransactionDetail(app_label=BookingConfig.name,
                                        model_name="invalid_model",
                                        pk=1)
            tx = TransactionInfo.objects.create(name=TransactionName.create_booking,
                                                details=details,
                                                user=self.user)

    def test_get_related_model(self):
        booking_record = BookingRecord.objects.create(user=self.user, start_time=self.now,
                                                      end_time=self.now + timedelta(days=1),
                                                      plane=self.plane)
        details = TransactionDetail(app_label=BookingConfig.name,
                                    model_name=BookingRecord.__name__,
                                    pk=booking_record.pk)
        tx = TransactionInfo.objects.create(name=TransactionName.create_booking,
                                            details=details,
                                            user=self.user)

        self.assertEquals(tx.get_related_object(), booking_record)
