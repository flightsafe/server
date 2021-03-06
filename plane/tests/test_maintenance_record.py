from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from common.constants import MaintenanceStatus
from transaction.models import TransactionInfo
from ..models import Plane, MaintenanceRecord, MaintenanceProgress, MaintenanceRecordItem


class MaintenanceRecordTestCase(TestCase):
    def setUp(self) -> None:
        self.plane = Plane.objects.create(title="Plane 1", description="Mock Plane")
        self.plane2 = Plane.objects.create(title="Plane 2", description="Mock Plane")
        self.time_1 = datetime(2020, 5, 31, tzinfo=timezone.utc)
        self.time_2 = datetime(2020, 6, 1, tzinfo=timezone.utc)
        self.time_3 = datetime(2020, 6, 2, tzinfo=timezone.utc)
        self.user = User.objects.create(username="mock_user")

    def test_maintenance_record_without_items(self):
        record = MaintenanceRecord.objects.create(plane=self.plane,
                                                  title="Test record",
                                                  description="Test description",
                                                  author=self.user)
        self.assertIsNone(record.start_time)
        self.assertIsNone(record.end_time)
        self.assertEqual(record.progress, MaintenanceProgress.pending.value)
        self.assertEquals(TransactionInfo.objects.count(), 1)

    def test_maintenance_record_without_items_2(self):
        record = MaintenanceRecord.objects.create(plane=self.plane,
                                                  title="Test record",
                                                  description="Test description",
                                                  progress=MaintenanceProgress.in_progress,
                                                  author=self.user)
        self.assertIsNone(record.start_time)
        self.assertIsNone(record.end_time)
        self.assertEqual(record.progress, MaintenanceProgress.in_progress)

    def test_maintenance_record_with_items_1(self):
        now = timezone.now()
        record = MaintenanceRecord.objects.create(plane=self.plane,
                                                  title="Test record",
                                                  description="Test description",
                                                  progress=MaintenanceProgress.in_progress,
                                                  author=self.user)
        MaintenanceRecordItem.objects.create(
            maintenance_record=record,
            title="item 1",
            description="description 1",
            start_time=now,
            operator=self.user
        )
        self.assertEquals(record.start_time.day, now.day)
        self.assertEquals(record.start_time.year, now.year)
        self.assertIsNone(record.end_time)
        self.assertEqual(record.progress, MaintenanceProgress.in_progress)

    def test_maintenance_record_with_items_2(self):
        record = MaintenanceRecord.objects.create(plane=self.plane,
                                                  title="Test record",
                                                  description="Test description",
                                                  progress=MaintenanceProgress.finished,
                                                  author=self.user)
        MaintenanceRecordItem.objects.create(
            maintenance_record=record,
            title="item 1",
            description="description 1",
            start_time=self.time_1,
            end_time=self.time_1,
            operator=self.user
        )

        MaintenanceRecordItem.objects.create(
            maintenance_record=record,
            title="item 2",
            description="description 2",
            start_time=self.time_2,
            end_time=self.time_2,
            operator=self.user
        )

        MaintenanceRecordItem.objects.create(
            maintenance_record=record,
            title="item 3",
            description="description 3",
            start_time=self.time_3,
            end_time=self.time_3,
            operator=self.user
        )

        self.assertEquals(record.start_time.day, self.time_1.day)
        self.assertEquals(record.start_time.month, self.time_1.month)
        self.assertEquals(record.start_time.year, self.time_1.year)

        self.assertEquals(record.end_time.day, self.time_3.day)
        self.assertEquals(record.end_time.month, self.time_3.month)
        self.assertEquals(record.end_time.year, self.time_3.year)

        self.assertEqual(record.progress, MaintenanceProgress.finished)
        self.assertEquals(record.status, MaintenanceStatus.good_condition)

    def test_expire(self):
        expire_time = timezone.now() - timedelta(days=2)

        record = MaintenanceRecord.objects.create(plane=self.plane,
                                                  title="Test record",
                                                  description="Test description",
                                                  progress=MaintenanceProgress.finished,
                                                  author=self.user)
        MaintenanceRecordItem.objects.create(
            maintenance_record=record,
            title="item 1",
            description="description 1",
            start_time=self.time_1,
            end_time=self.time_1,
            operator=self.user
        )

        MaintenanceRecordItem.objects.create(
            maintenance_record=record,
            title="item 2",
            description="description 2",
            start_time=self.time_2,
            end_time=self.time_2,
            operator=self.user
        )

        MaintenanceRecordItem.objects.create(
            maintenance_record=record,
            title="item 3",
            description="description 3",
            start_time=self.time_3,
            end_time=self.time_3,
            expire_at=expire_time,
            operator=self.user
        )

        self.assertEquals(record.start_time.day, self.time_1.day)
        self.assertEquals(record.start_time.month, self.time_1.month)
        self.assertEquals(record.start_time.year, self.time_1.year)

        self.assertEquals(record.end_time.day, self.time_3.day)
        self.assertEquals(record.end_time.month, self.time_3.month)
        self.assertEquals(record.end_time.year, self.time_3.year)

        self.assertEqual(record.progress, MaintenanceProgress.finished)
        self.assertEquals(record.status, MaintenanceStatus.expired.value)

    def test_expire_2(self):
        expire_time = timezone.now() + timedelta(days=2)

        record = MaintenanceRecord.objects.create(plane=self.plane,
                                                  title="Test record",
                                                  description="Test description",
                                                  progress=MaintenanceProgress.finished,
                                                  author=self.user)
        MaintenanceRecordItem.objects.create(
            maintenance_record=record,
            title="item 1",
            description="description 1",
            start_time=self.time_1,
            end_time=self.time_1,
            operator=self.user
        )

        MaintenanceRecordItem.objects.create(
            maintenance_record=record,
            title="item 2",
            description="description 2",
            start_time=self.time_2,
            end_time=self.time_2,
            operator=self.user
        )

        MaintenanceRecordItem.objects.create(
            maintenance_record=record,
            title="item 3",
            description="description 3",
            start_time=self.time_3,
            end_time=self.time_3,
            expire_at=expire_time,
            operator=self.user
        )

        self.assertEquals(record.start_time.day, self.time_1.day)
        self.assertEquals(record.start_time.month, self.time_1.month)
        self.assertEquals(record.start_time.year, self.time_1.year)

        self.assertEquals(record.end_time.day, self.time_3.day)
        self.assertEquals(record.end_time.month, self.time_3.month)
        self.assertEquals(record.end_time.year, self.time_3.year)

        self.assertEqual(record.progress, MaintenanceProgress.finished)
        self.assertEquals(record.status, MaintenanceStatus.good_condition)

    def test_expire_3(self):
        expire_time = timezone.now() - timedelta(days=2)
        expire_time_2 = timezone.now() + timedelta(days=2)

        record = MaintenanceRecord.objects.create(plane=self.plane,
                                                  title="Test record",
                                                  description="Test description",
                                                  progress=MaintenanceProgress.finished,
                                                  author=self.user)
        MaintenanceRecordItem.objects.create(
            maintenance_record=record,
            title="item 1",
            description="description 1",
            start_time=self.time_1,
            end_time=self.time_1,
            operator=self.user
        )

        MaintenanceRecordItem.objects.create(
            maintenance_record=record,
            title="item 2",
            description="description 2",
            start_time=self.time_2,
            end_time=self.time_2,
            expire_at=expire_time,
            operator=self.user
        )

        MaintenanceRecordItem.objects.create(
            maintenance_record=record,
            title="item 3",
            description="description 3",
            start_time=self.time_3,
            end_time=self.time_3,
            expire_at=expire_time_2,
            operator=self.user,
        )

        self.assertEquals(record.start_time.day, self.time_1.day)
        self.assertEquals(record.start_time.month, self.time_1.month)
        self.assertEquals(record.start_time.year, self.time_1.year)

        self.assertEquals(record.end_time.day, self.time_3.day)
        self.assertEquals(record.end_time.month, self.time_3.month)
        self.assertEquals(record.end_time.year, self.time_3.year)

        self.assertEqual(record.progress, MaintenanceProgress.finished)
        self.assertEquals(record.status, MaintenanceStatus.expired.value)
