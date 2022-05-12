from datetime import datetime

from django.test import TestCase

from ..models import Plane, MaintenanceRecord, MaintenanceStatus, MaintenanceRecordItem


class MaintenanceRecordTestCase(TestCase):
    def setUp(self) -> None:
        self.plane = Plane.objects.create(name="Plane 1", description="Mock Plane")
        self.plane2 = Plane.objects.create(name="Plane 2", description="Mock Plane")

    def test_maintenance_record_without_items(self):
        record = MaintenanceRecord.objects.create(plane=self.plane,
                                                  name="Test record",
                                                  description="Test description")
        self.assertIsNone(record.start_time)
        self.assertIsNone(record.end_time)
        self.assertEqual(record.status, MaintenanceStatus.pending)

    def test_maintenance_record_without_items_2(self):
        record = MaintenanceRecord.objects.create(plane=self.plane,
                                                  name="Test record",
                                                  description="Test description",
                                                  status=MaintenanceStatus.in_progress)
        self.assertIsNone(record.start_time)
        self.assertIsNone(record.end_time)
        self.assertEqual(record.status, MaintenanceStatus.in_progress)

    def test_maintenance_record_with_items_1(self):
        now = datetime.now()
        record = MaintenanceRecord.objects.create(plane=self.plane,
                                                  name="Test record",
                                                  description="Test description",
                                                  status=MaintenanceStatus.in_progress)
        MaintenanceRecordItem.objects.create(
            maintenance_record=record,
            name="item 1",
            description="description 1",
            start_time=now
        )
        self.assertEquals(record.start_time.day, now.day)
        self.assertEquals(record.start_time.year, now.year)
        self.assertIsNone(record.end_time)
        self.assertEqual(record.status, MaintenanceStatus.in_progress)

    def test_maintenance_record_with_items_2(self):
        time_1 = datetime(2020, 5, 31)
        time_2 = datetime(2020, 6, 1)
        time_3 = datetime(2020, 6, 2)

        record = MaintenanceRecord.objects.create(plane=self.plane,
                                                  name="Test record",
                                                  description="Test description",
                                                  status=MaintenanceStatus.finished)
        MaintenanceRecordItem.objects.create(
            maintenance_record=record,
            name="item 1",
            description="description 1",
            start_time=time_1,
            end_time=time_1
        )

        MaintenanceRecordItem.objects.create(
            maintenance_record=record,
            name="item 2",
            description="description 2",
            start_time=time_2,
            end_time=time_2
        )

        MaintenanceRecordItem.objects.create(
            maintenance_record=record,
            name="item 3",
            description="description 3",
            start_time=time_3,
            end_time=time_3
        )

        self.assertEquals(record.start_time.day, time_1.day)
        self.assertEquals(record.start_time.month, time_1.month)
        self.assertEquals(record.start_time.year, time_1.year)

        self.assertEquals(record.end_time.day, time_3.day)
        self.assertEquals(record.end_time.month, time_3.month)
        self.assertEquals(record.end_time.year, time_3.year)

        self.assertEqual(record.status, MaintenanceStatus.finished)
