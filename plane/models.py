"""
Plane app: stored plane's info and maintenance record
"""


from typing import Optional

from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models import Q

from plane.constants import MaintenanceProgress, MaintenanceStatus


class Plane(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField()
    image = models.ImageField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.updated_time = datetime.datetime.now()
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.name


class MaintenanceRecord(models.Model):
    name = models.CharField(max_length=128, default="maintenance")
    description = models.TextField(help_text="Maintenance record description")
    plane = models.ForeignKey(Plane, on_delete=models.CASCADE, related_name="records")
    progress = models.CharField(
        choices=[
            (MaintenanceProgress.pending.value, "pending"),
            (MaintenanceProgress.in_progress.value, "in progress"),
            (MaintenanceProgress.finished.value, "finished")
        ],
        default=MaintenanceProgress.pending,
        max_length=128
    )

    @property
    def status(self) -> MaintenanceStatus:
        now = datetime.datetime.now()
        is_exist = MaintenanceRecordItem.objects.filter(Q(maintenance_record=self) & Q(expire_at__lt=now)).exists()
        return MaintenanceStatus.expired if is_exist else MaintenanceStatus.good_condition

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
        return self.name


class MaintenanceRecordItem(models.Model):
    maintenance_record = models.ForeignKey(MaintenanceRecord, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=128)
    description = models.TextField()
    image = models.ImageField(blank=True, null=True)
    operator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True, blank=True)
    expire_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
