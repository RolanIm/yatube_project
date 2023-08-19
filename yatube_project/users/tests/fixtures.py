from django.test import TestCase, Client
from django.contrib.auth import get_user_model

User = get_user_model()


class TestUsers(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            username='test-user',
            password='test-password',
            email='test-email'
        )

    def setUp(self):
        self.guest_client = Client()
        self.auth_client = Client()
        self.auth_client.force_login(self.user)
