from django.db import models
from django.contrib.auth.models import User

from common.constants import ErrorCode
from plane import models as plane
from django.core import exceptions
from django.utils.translation import gettext_lazy as _


class BookingRecord(models.Model):
    plane = models.ForeignKey(plane.Plane, on_delete=models.CASCADE, related_name="bookings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.start_time >= self.end_time:
            raise exceptions.ValidationError({
                "start_time": exceptions.ValidationError(_("Start time should not greater or equal to end_time"),
                                                         code=ErrorCode.invalid)
            })
        is_available = self.plane.is_available(start_time=self.start_time, end_time=self.end_time)
        if not is_available:
            raise exceptions.ValidationError({
                "plane": exceptions.ValidationError(_(f"Plane is in use during {self.start_time} and {self.end_time}"),
                                                    code=ErrorCode.invalid)
            })

        super().save(force_insert, force_update, using, update_fields)
