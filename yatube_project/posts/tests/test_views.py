from .fixtures import TestPosts
from django.urls import reverse

from ..models import Follow


class ViewsTestsPosts(TestPosts):
    def test_reverse_use_correct_templates(self):
        username = self.user.username
        reverse_template = {
            reverse('posts:post_list'): 'posts/post_list.html',
            reverse('posts:post_create'): 'posts/post_form.html',
            reverse(
                'posts:group_posts',
                kwargs={'slug': self.group.slug}): 'posts/group_list.html',
            reverse(
                'posts:profile',
                kwargs={'username': username}): 'posts/profile.html',
            reverse(
                'posts:post_detail',
                kwargs={'pk': self.post.id}): 'posts/post_detail.html',
            reverse(
                'posts:post_edit',
                kwargs={'pk': self.post.id}): 'posts/post_form.html',
            reverse('posts:follow_list'): 'posts/follow_post_list.html',
        }

        for reverse_url, expected_template in reverse_template.items():
            with self.subTest(reverse_name=reverse_url):
                response = self.auth_client.get(reverse_url)
                self.assertTemplateUsed(response, expected_template)

    def test_correct_index_view_context(self):
        response_1 = self.auth_client.get(reverse('posts:post_list'))
        page_obj = response_1.context['page_obj']
        post_text = page_obj[0].text
        self.assertEqual(post_text, self.other_post.text)
        self.assertEqual(len(page_obj), 10)
        response_2 = self.auth_client.get(reverse('posts:post_list')+'?page=2')
        self.assertEqual(len(response_2.context['page_obj']), 2)

    def test_correct_group_posts_view_context(self):
        response_1 = self.auth_client.get(
            reverse('posts:group_posts', args=['slug-1'])
        )
        page_obj = response_1.context['page_obj']
        post_image = page_obj[0].image
        for obj in page_obj:
            with self.subTest(obj=obj.text[:20]):
                self.assertEqual(obj.group, response_1.context['group'])
        self.assertEqual(len(page_obj), 10)
        response_2 = self.auth_client.get(
            reverse('posts:group_posts', args=['slug-1']) + '?page=2')
        self.assertEqual(len(response_2.context['page_obj']), 1)
        self.assertEqual(post_image, self.posts[-1].image)

    def test_correct_profile_view_context(self):
        response_1 = self.auth_client.get(reverse(
            'posts:profile', args=[self.user]
        ))
        author = response_1.context['author_obj']
        page_obj = response_1.context['page_obj']
        count_posts = response_1.context['paginator'].count
        post_image = page_obj[0].image
        self.assertEqual(author, self.user)
        self.assertEqual(count_posts, len(self.posts))
        self.assertEqual(len(page_obj), 10)
        response_2 = self.auth_client.get(reverse(
            'posts:profile', args=[self.user]
        ) + '?page=2')
        self.assertEqual(len(response_2.context['page_obj']), 1)
        self.assertEqual(post_image, self.posts[-1].image)

    def test_correct_post_detail_view_context(self):
        response = self.auth_client.get(reverse('posts:post_detail', args=[1]))
        post = response.context['post']
        self.assertEqual(post.id, 1)
        self.assertEqual(post.image, self.post.image)

    def test_correct_create_post_view_context(self):
        response = self.auth_client.get(reverse('posts:post_create'))
        for field, expected_type in self.form_fields.items():
            with self.subTest(field_name=field):
                form_field = response.context['form'].fields[field]
                self.assertIsInstance(form_field, expected_type)

    def test_show_post_on_each_page(self):
        reverse_urls = [
            reverse('posts:post_list'),
            reverse('posts:group_posts', args=[self.group.slug]),
            reverse('posts:profile', args=[self.user]),
        ]
        for reverse_url in reverse_urls:
            with self.subTest(reverse_url=reverse_url):
                response = self.auth_client.get(reverse_url)
                last_object = response.context['page_obj'][0]
                expected_last_id = 12 if reverse_url == '/' else 11
                self.assertEqual(last_object.id, expected_last_id)

        other_group_slug = self.other_group.slug
        reverse_url_other = reverse('posts:group_posts',
                                    args=[other_group_slug]
                                    )
        response = self.auth_client.get(reverse_url_other)
        self.assertEqual(len(response.context['page_obj']), 1)

    def test_correct_update_post_view_context(self):
        response = self.auth_client.get(reverse('posts:post_edit', args=[1]))
        for field, expected_type in self.form_fields.items():
            with self.subTest(field_name=field):
                form_field = response.context['form'].fields[field]
                self.assertIsInstance(form_field, expected_type)

    def test_show_image_on_each_page(self):
        urls = [
            reverse('posts:post_list'),
            reverse('posts:group_posts', args=[self.group.slug]),
            reverse('posts:profile', args=[self.user]),
            reverse('posts:post_detail', args=[self.posts[-1].id]),
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.auth_client.get(url)
                if url == '/posts/11/':
                    last_object = response.context['post']
                else:
                    last_object = response.context['page_obj'][0]
                self.assertTrue(last_object.image)

    def test_correct_profile_follow_view(self):
        url = reverse('posts:follow_list')
        response1 = self.auth_client.get(url)
        follow_list_post = response1.context['page_obj'][0]
        self.assertEqual(self.other_post, follow_list_post)

        response2 = self.auth_client2.get(url)
        is_objects = response2.context['page_obj']
        self.assertFalse(is_objects)

        url = reverse('posts:profile_follow',
                      kwargs={'username': self.user.username})
        self.auth_client2.get(url)
        is_objects = Follow.objects.filter(
            user=self.user2, author=self.user).exists()
        self.assertTrue(is_objects)

    def test_correct_profile_unfollow_view(self):
        url = reverse('posts:profile_unfollow',
                      kwargs={'username': self.user2.username})
        self.auth_client.get(url)
        is_objects = Follow.objects.filter(
            user=self.user, author=self.user2).exists()
        self.assertFalse(is_objects)
