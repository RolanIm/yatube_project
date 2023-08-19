from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from ..models import Post, Group

User = get_user_model()


class TestPosts(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            username='test-username',
            password='test-password',
            email='test@gmail.com'
        )
        cls.user2 = User.objects.create(username='not-owner-user')
        cls.group = Group.objects.create(
            title='title-1',
            slug='slug-1',
            description='description-1')
        cls.other_group = Group.objects.create(
            title='title-2',
            slug='slug-2',
            description='description-2')
        cls.posts = list()
        for _ in range(11):
            cls.posts.append(
                Post.objects.create(text=f'text-1',
                                    author=cls.user,
                                    group=cls.group)
            )
        cls.post = cls.posts[0]

    def setUp(self):
        self.guest_client = Client()
        self.auth_client = Client()
        self.auth_client2 = Client()
        self.auth_client.force_login(self.user)
        self.auth_client2.force_login(self.user2)
        self.redirect_url = reverse(
            'posts:profile',
            kwargs={'username': self.user.username}
        )

