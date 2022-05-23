from datetime import timedelta
from http import HTTPStatus
from io import BytesIO

from PIL import Image
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase

from booking.models import BookingRecord
from course.models import Course
from course.models import Lesson, LessonHistory, Comment
from plane.models import Plane, MaintenanceRecord, MaintenanceRecordItem
from transaction.models import TransactionInfo, TransactionName


def temporary_image():
    bts = BytesIO()
    img = Image.new("RGB", (100, 100))
    img.save(bts, 'jpeg')
    return SimpleUploadedFile("test.jpg", bts.getvalue())


class E2ETesting(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="mock_user", password="mock_password")
        self.client.force_login(self.user)
        self.now = timezone.now()

    def test_basic_browsing(self):
        # create a plane
        url = reverse("plane-list")
        response = self.client.post(url, data={"name": "Test Plane", "description": "Test Description",
                                               "image": temporary_image()}, format="multipart")
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Plane.objects.count(), 1)

        url = reverse("plane-detail", kwargs={"pk": Plane.objects.first().pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data["name"], "Test Plane")
        self.assertEqual(response.data["description"], "Test Description")

        # Create a maintenance record
        url = reverse("maintenance-list")
        response = self.client.post(url, data={"plane": Plane.objects.first().pk, "description": "Test Description",
                                               "image": temporary_image()}, format="multipart")
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(MaintenanceRecord.objects.count(), 1)

        # Create a maintenance record item
        url = reverse("maintenance-item-list")
        response = self.client.post(url, data={"maintenance_record": MaintenanceRecord.objects.first().pk,
                                               "description": "Test Description", "image": temporary_image(),
                                               "name": "Test item"},
                                    format="multipart")
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(MaintenanceRecordItem.objects.count(), 1)

        # create a course
        url = reverse("course-list")
        response = self.client.post(url, data={"name": "Test Course", "description": "Test Description"})
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Course.objects.count(), 1)

        # create a lesson
        url = reverse("lesson-list")
        response = self.client.post(url, data={"name": "Test Lesson", "description": "Test Description",
                                               "course": 1}, format="multipart")
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Lesson.objects.count(), 1)

        # create a lesson history
        url = reverse("lesson-history-list")
        response = self.client.post(url, data={"lesson": 1, "plane": 1, "start_time": self.now,
                                               "end_time": self.now + timedelta(days=1)}, format="json")
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(LessonHistory.objects.count(), 1)

        # create a comment
        url = reverse("comment-list")
        response = self.client.post(url, data={"lesson_history": 1, "plane": 1, "comment": "Hello world"},
                                    format="json")
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Comment.objects.count(), 1)

        self.assertEquals(BookingRecord.objects.count(), 1)
        self.assertEqual(TransactionInfo.objects.count(), 4)

        transactions = TransactionInfo.objects.all()
        self.assertEqual(transactions[0].name, TransactionName.add_maintenance_item)
        self.assertEqual(transactions[1].name, TransactionName.add_maintenance_item)
        self.assertEqual(transactions[2].name, TransactionName.create_lesson_record)
        self.assertEqual(transactions[3].name, TransactionName.create_booking)
