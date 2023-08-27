from django.urls import reverse
from .fixtures import TestPosts
from ..models import Post, Comment


class TestPostsForms(TestPosts):
    def test_correct_create_post_form(self):
        posts_count = Post.objects.count()
        form_data = {
            'title': 'title-text',
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
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.filter(
                title='title-text',
                author=self.user,
                text='text-new',
                group=self.group,
            ).exists()
        )

    def test_correct_edit_post_form(self):
        posts_count = Post.objects.count()
        form_data = {
            'title': 'title-text-updated',
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
                title='title-text-updated',
                author=self.user,
                text='text-updated',
                group=self.group,
            ).exists()
        )

    def test_comment_only_for_auth(self):
        comments_count = self.post.comments.count()
        form_data = {
            'text': 'text-comment',
            'author': self.user,
            'post': self.post,
        }
        reverse_urls = {
            'get': reverse('posts:post_detail', args=[self.post.id]),
            'post': reverse('posts:add_comment', args=[self.post.id]),
        }
        redirect_url = reverse(
            'posts:post_detail',
            kwargs={'pk': self.post.id}
        )
        for method, reverse_url in reverse_urls.items():
            with self.subTest(reverse_url=reverse_url):
                if method == 'get':
                    # get request for guest client
                    response_get_guest = self.guest_client.get(reverse_url)
                    self.assertIsNotNone(response_get_guest.context['form'])
                else:
                    # post request for guest client
                    self.guest_client.post(reverse_url,
                                           data=form_data,
                                           follow=True)
                    self.assertEqual(Comment.objects.count(),
                                     comments_count)
                    # post request for authenticated client
                    response_post_auth = self.auth_client.post(reverse_url,
                                                               data=form_data,
                                                               follow=True)
                    self.assertEqual(Comment.objects.count(),
                                     comments_count + 1)
                    self.assertRedirects(response_post_auth, redirect_url)
                    self.assertTrue(
                        Comment.objects.filter(
                            author=self.user,
                            text='text-comment',
                            post=self.post
                        ).exists()
                    )
