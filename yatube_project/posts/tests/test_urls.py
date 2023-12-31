from http import HTTPStatus
from .fixtures import TestPosts
from time import sleep


class URLTestsPosts(TestPosts):
    def test_correct_url_path_for_all(self):
        post = self.post
        group = self.group
        urls = [
            '/',
            f'/group/{group.slug}/',
            f'/posts/{post.pk}/',
            '/unexciting_page/',
        ]
        guest_client = self.guest_client
        for url in urls:
            response = guest_client.get(url)
            if url == '/unexciting_page/':
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
            else:
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_correct_url_path_for_auth(self):
        post = self.post
        urls = [
            f'/profile/{self.user.username}/',
            f'/posts/{post.pk}/edit',
            '/create/',
            '/follow/',
        ]
        guest_client = self.guest_client
        auth_client = self.auth_client
        auth_client2 = self.auth_client2
        for url in urls:
            with self.subTest(url=url):
                if 'edit' in url:
                    response = auth_client2.get(url)
                    self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
                    response = guest_client.get(url)
                    self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
                else:
                    response = guest_client.get(url)
                    self.assertRedirects(
                        response,
                        f'/auth/login/?next={url}')
                    response = auth_client.get(url)
                    self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_template(self):
        post = self.post
        urls_and_templates = {
            '/': 'posts/post_list.html',
            f'/group/{self.group.slug}/': 'posts/group_list.html',
            f'/profile/{self.user}/': 'posts/profile.html',
            f'/posts/{post.pk}/': 'posts/post_detail.html',
            '/create/': 'posts/post_form.html',
            f'/posts/{post.pk}/edit': 'posts/post_form.html',
            f'/follow/': 'posts/follow_post_list.html',
        }
        auth_client = self.auth_client
        for url, template in urls_and_templates.items():
            with self.subTest(url=url):
                response = auth_client.get(url)
                self.assertTemplateUsed(response, template)
