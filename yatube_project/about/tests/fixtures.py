from django.test import TestCase, Client
from django.contrib.auth import get_user_model


class TestAbout(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
