from http import HTTPStatus
from .fixtures import TestAbout


class URLTestsAbout(TestAbout):
    def test_correct_url(self):
        urls_and_templates = {
            '/about/author/': 'about/author.html',
            '/about/tech/': 'about/tech.html'
        }
        for url, expected_template in urls_and_templates.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertTemplateUsed(response, expected_template)
