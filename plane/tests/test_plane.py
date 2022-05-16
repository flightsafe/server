from django.test import TestCase

from ..models import Plane


class PlaneTestCase(TestCase):
    def test_create_model(self):
        Plane.objects.create(name="Plane", description="Test redoc")
        self.assertEqual(Plane.objects.count(), 1)

    def test_update_model(self):
        plane = Plane.objects.create(name="Plane", description="Test redoc")
        plane.name = "Plane 2"
        plane.save()

        self.assertEqual(Plane.objects.count(), 1)
        new_plane = Plane.objects.get(id=plane.id)
        self.assertEqual(new_plane.name, plane.name)
