from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from course import models as course
from plane import models as plane


class BookingRecord(models.Model):
    plane = models.ForeignKey(plane.Plane, on_delete=models.CASCADE, related_name="bookings")
    lesson = models.ForeignKey(course.LessonHistory, null=True, blank=True, help_text=_("Used in the lesson"),
                               on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.start_time
