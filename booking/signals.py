from django.core import exceptions
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from booking.models import BookingRecord
from common.constants import ErrorCode


@receiver(pre_save, sender=BookingRecord)
def validating_booking_record(sender, instance: BookingRecord, **kwargs):
    if instance.start_time >= instance.end_time:
        raise exceptions.ValidationError({
            "start_time": exceptions.ValidationError(_("Start time should not greater or equal to end_time"),
                                                     code=ErrorCode.invalid)
        })
    is_available = instance.plane.is_available(start_time=instance.start_time, end_time=instance.end_time)
    if not is_available:
        raise exceptions.ValidationError({
            "plane": exceptions.ValidationError(
                _(f"Plane is in use during {instance.start_time} and {instance.end_time}"),
                code=ErrorCode.invalid)
        })
