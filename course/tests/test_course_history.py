from datetime import timedelta

from django.contrib.auth.models import User
from django.core import exceptions
from django.test import TestCase
from django.utils import timezone

from booking.models import BookingRecord
from course.models import Course, Lesson, LessonHistory
from plane.models import Plane


class TestCourseHistory(TestCase):
    def setUp(self) -> None:
        self.plane = Plane.objects.create(name="plane")
        self.now = timezone.now()
        self.course = Course.objects.create(name="Course 1", description="Course 1")
        self.lesson = Lesson.objects.create(course=self.course, name="Lesson", description="Lesson")
        self.user = User.objects.create(username="user")

    def test_create(self):
        lesson_history = LessonHistory.objects.create(plane=self.plane, start_time=self.now,
                                                      end_time=self.now + timedelta(days=1),
                                                      student=self.user)
        self.assertEquals(LessonHistory.objects.count(), 1)
        self.assertEquals(BookingRecord.objects.count(), 1)
        bookings = BookingRecord.objects.all()[0]
        self.assertEquals(bookings.lesson, lesson_history)

    def test_create_failed(self):
        BookingRecord.objects.create(start_time=self.now - timedelta(days=1), end_time=self.now + timedelta(days=2),
                                     plane=self.plane, user=self.user)
        with self.assertRaises(expected_exception=exceptions.ValidationError):
            LessonHistory.objects.create(plane=self.plane, start_time=self.now,
                                         end_time=self.now + timedelta(days=1),
                                         student=self.user)

        self.assertEquals(LessonHistory.objects.count(), 0)
        self.assertEquals(BookingRecord.objects.count(), 1)

    def test_delete(self):
        lesson_history = LessonHistory.objects.create(plane=self.plane, start_time=self.now,
                                                      end_time=self.now + timedelta(days=1),
                                                      student=self.user,
                                                      grade=100)
        self.assertEquals(BookingRecord.objects.count(), 1)
        lesson_history.delete()
        self.assertEquals(LessonHistory.objects.count(), 0)
        self.assertEquals(BookingRecord.objects.count(), 0)
