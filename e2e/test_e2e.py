from django.contrib.auth.models import User
from django.test import TestCase


class E2ETesting(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="mock_user")

    def test_basic_browsing(self):
        pass
