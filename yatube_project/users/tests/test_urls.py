from http import HTTPStatus
from .fixtures import TestUsers


class URLTestsUsers(TestUsers):
    def test_urls_uses_correct_template(self):
        urls_and_templates = {
            '/auth/signup/': 'users/signup.html',
            '/auth/logout/': 'users/logged_out.html',
            '/auth/login/': 'users/login.html',
            '/auth/password_reset/': 'users/password_reset_form.html',
            '/auth/password_reset/done/': 'users/password_reset_done.html',
            '/auth/reset/done/': 'users/password_reset_complete.html',
        }
        for url, template in urls_and_templates.items():
            with self.subTest(url=url):
                response = self.auth_client.get(url, follow=True)
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertTemplateUsed(response, template)
