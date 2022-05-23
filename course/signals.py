from django.core import exceptions
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from booking import models as booking
from common.constants import TransactionName
from common.types import TransactionDetail
from course.apps import CourseConfig
from course.models import LessonHistory
from transaction.models import TransactionInfo


@receiver(pre_save, sender=LessonHistory)
def validating_lesson_history(sender, instance: LessonHistory, **kwargs):
    if instance.grade:
        if instance.grade < 0 or instance.grade > 100:
            raise exceptions.ValidationError({
                "grade": exceptions.ValidationError(_("Grade must in range from 0 to 100"))
            })


@receiver(post_save, sender=LessonHistory)
def update_booking_record(sender, instance: LessonHistory, **kwargs):
    """
    Create a booking record when a new lesson history is created.
    Will delete the created lesson history if booking failed.
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    try:
        detail = TransactionDetail(app_label=CourseConfig.name, model_name=LessonHistory.__name__, pk=instance.pk)
        TransactionInfo.objects.create(name=TransactionName.create_lesson_record, details=detail, user=instance.student)
        booking.BookingRecord.objects.create(plane=instance.plane, start_time=instance.start_time,
                                             end_time=instance.end_time, user=instance.student, lesson=instance)
    except Exception as e:
        instance.delete()
        raise e
