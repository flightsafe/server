"""
Plane app: stored plane's info and maintenance record
"""

import datetime
from typing import Optional

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.utils import timezone

from common.constants import MaintenanceProgress, MaintenanceStatus, BookingStatus


class Plane(models.Model):
    title = models.CharField(max_length=128, unique=True)
    description = models.TextField()
    image = models.ImageField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.updated_time = timezone.now()
        super().save(force_insert, force_update, using, update_fields)

    def is_available(self, start_time: datetime.datetime, end_time: datetime.datetime) -> bool:
        """
        Returns the if the plane is available during the time range
        :param start_time:
        :param end_time:
        :return: true if the plane is available
        """
        is_in_use = self.bookings.filter(Q(start_time__lte=start_time) & Q(end_time__gte=end_time)).exists()
        return not is_in_use

    @property
    def booking_status(self) -> BookingStatus:
        """
        Returns the currently booking status of the plane
        :return:
        """
        now = timezone.now()
        is_available = self.is_available(now, now)
        if not is_available:
            return BookingStatus.in_use
        return BookingStatus.not_in_use

    def __str__(self):
        return self.title


class MaintenanceRecord(models.Model):
    title = models.CharField(max_length=128, default="maintenance")
    description = models.TextField(help_text="Maintenance record description")
    plane = models.ForeignKey(Plane, on_delete=models.CASCADE, related_name="records")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    progress = models.CharField(
        choices=MaintenanceProgress.choices,
        default=MaintenanceProgress.pending.value,
        max_length=128
    )

    @property
    def status(self) -> MaintenanceStatus:
        now = timezone.now()
        is_expired = MaintenanceRecordItem.objects.filter(Q(maintenance_record=self) & Q(expire_at__lt=now)).exists()
        is_bad = MaintenanceRecordItem.objects.filter(
            Q(maintenance_record=self) & Q(status=MaintenanceStatus.bad_condition)).exists()
        if is_expired:
            return MaintenanceStatus.expired.value
        if is_bad:
            return MaintenanceStatus.expired.value
        return MaintenanceStatus.expired.good_condition

    @property
    def start_time(self) -> Optional[datetime.datetime]:
        """
        Get the maintenance start time
        :return:
        """
        if self.progress == MaintenanceProgress.pending:
            return None
        if MaintenanceRecordItem.objects.filter(maintenance_record=self).count() > 0:
            first_record = MaintenanceRecordItem.objects \
                .filter(maintenance_record=self) \
                .order_by("start_time")[0]
            return first_record.start_time

        return None

    @property
    def end_time(self):
        """
        Get the maintenance end time
        :return:
        """
        if self.progress == MaintenanceProgress.finished:
            if MaintenanceRecordItem.objects.filter(maintenance_record=self).count() > 0:
                last_record = MaintenanceRecordItem.objects \
                    .filter(maintenance_record=self) \
                    .order_by("-end_time")[0]
                return last_record.end_time
        return None

    def __str__(self):
        return self.title


class MaintenanceRecordItem(models.Model):
    maintenance_record = models.ForeignKey(MaintenanceRecord, on_delete=models.CASCADE, related_name="items")
    title = models.CharField(max_length=128)
    description = models.TextField()
    image = models.ImageField(blank=True, null=True)
    operator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True, blank=True)
    expire_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=128,
                              choices=MaintenanceStatus.choices,
                              default=MaintenanceStatus.good_condition)

    def __str__(self):
        return self.title
