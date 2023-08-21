from django.urls import reverse
from .fixtures import TestPosts
from ..models import Post


class TestPostsForms(TestPosts):
    def test_correct_create_form(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'text-new',
            'group': self.group.pk,
            'image': self.post.image,
        }
        response = self.auth_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, self.redirect_url)
        self.assertEqual(Post.objects.count(), posts_count+1)
        self.assertTrue(
            Post.objects.filter(
                author=self.user,
                text='text-new',
                group=self.group,
            ).exists()
        )

    def test_correct_edit_form(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'text-updated',
            'group': self.group.pk,
            'image': self.post.image,
        }
        response = self.auth_client.post(
            reverse('posts:post_edit', args=[self.post.id]),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, self.redirect_url)
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertTrue(
            Post.objects.filter(
                author=self.user,
                text='text-updated',
                group=self.group,
            ).exists()
        )
