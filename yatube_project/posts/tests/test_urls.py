from http import HTTPStatus
from .fixtures import TestPosts


class URLTestsPosts(TestPosts):
    def test_correct_url_path(self):
        post = self.post
        group = self.group
        urls = [
            '/',
            f'/group/{group.slug}/',
            f'/profile/{self.user.username}/',
            f'/posts/{post.pk}/',
            '/unexciting_page/',
            f'/posts/{post.pk}/edit',
            '/create/',
        ]
        guest_client = self.guest_client
        auth_client = self.auth_client
        for url in urls:
            with self.subTest(url=url):
                if url not in (f'/profile/{self.user.username}/',
                               f'/posts/{post.pk}/edit',
                               '/create/'):
                    response = guest_client.get(url)
                if url == '/unexciting_page/':
                    self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
                elif url == f'/posts/{post.pk}/edit':
                    response = guest_client.get(url)
                    self.assertRedirects(
                        response,
                        f'/auth/login/?next={url}')
                    response = auth_client.get(url)
                    self.assertEqual(response.status_code, HTTPStatus.OK)
                elif url in ('/create/', f'/profile/{self.user.username}/'):
                    response = auth_client.get(url)
                    self.assertEqual(response.status_code, HTTPStatus.OK)
                    response = guest_client.get(url)
                    self.assertRedirects(
                        response,
                        f'/auth/login/?next={url}')
                else:
                    self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_template(self):
        post = self.post
        urls_and_templates = {
            '/': 'posts/index.html',
            f'/group/{self.group.slug}/': 'posts/group_list.html',
            f'/profile/{self.user.username}/': 'posts/profile.html',
            f'/posts/{post.pk}/': 'posts/post_detail.html',
            '/create/': 'posts/create_post.html',
            f'/posts/{post.pk}/edit': 'posts/create_post.html'
        }
        auth_client = self.auth_client
        for url, template in urls_and_templates.items():
            with self.subTest(url=url):
                response = auth_client.get(url)
                self.assertTemplateUsed(response, template)
