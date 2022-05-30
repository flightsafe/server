from django.core import exceptions
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from booking.apps import BookingConfig
from booking.models import BookingRecord
from common.constants import ErrorCode, TransactionName
from common.types import TransactionDetail
from transaction.models import TransactionInfo


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


@receiver(post_save, sender=BookingRecord)
def write_transaction(sender, instance: BookingRecord, **kwargs):
    detail = TransactionDetail(app_label=BookingConfig.name, model_name=BookingRecord.__name__, pk=instance.pk)
    TransactionInfo.objects.create(title=TransactionName.create_booking, details=detail, user=instance.user)
