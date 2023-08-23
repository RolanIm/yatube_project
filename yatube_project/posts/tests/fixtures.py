from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client, override_settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings
from django import forms

import shutil
import tempfile

from ..models import Post, Group, Comment

User = get_user_model()
TEMP_MEDIA_ROOT = tempfile.mktemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TestPosts(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
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
        cls.form_fields = {
            'text': forms.CharField,
            'group': forms.ModelChoiceField,
            'image': forms.ImageField,
        }
        cls.redirect_url = reverse(
            'posts:profile',
            kwargs={'username': cls.user.username}
        )

    def setUp(self) -> None:
        small_gif = (
             b'\x47\x49\x46\x38\x39\x61\x02\x00'
             b'\x01\x00\x80\x00\x00\x00\x00\x00'
             b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
             b'\x00\x00\x00\x2C\x00\x00\x00\x00'
             b'\x02\x00\x01\x00\x00\x02\x02\x0C'
             b'\x0A\x00\x3B'
        )
        uploaded_img = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )

        self.posts = list()
        for num in range(11):
            self.posts.append(
                Post.objects.create(text=f'text-{num}',
                                    author=self.user,
                                    image=uploaded_img,
                                    group=self.group)
            )
        self.post = self.posts[0]
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            text='comment01'
        )

        self.guest_client = Client()
        self.auth_client = Client()
        self.auth_client2 = Client()
        self.auth_client.force_login(self.user)
        self.auth_client2.force_login(self.user2)

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
