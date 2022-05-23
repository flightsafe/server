from django.core import exceptions
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from booking import models as booking
from course.models import LessonHistory


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
        booking.BookingRecord.objects.create(plane=instance.plane, start_time=instance.start_time,
                                             end_time=instance.end_time, user=instance.student, lesson=instance)
        bookings = booking.BookingRecord.objects.all()[0]
        print(bookings)
    except Exception as e:
        instance.delete()
        raise e
