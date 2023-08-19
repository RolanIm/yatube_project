from django.urls import reverse
from .fixtures import TestAbout


class ViewsTestsAbout(TestAbout):
    def test_reverse_use_correct_templates(self):
        reverse_template = {
            reverse('about:author'): 'about/author.html',
            reverse('about:tech'): 'about/tech.html',
        }

        for reverse_url, expected_template in reverse_template.items():
            with self.subTest(reverse_name=reverse_url):
                response = self.guest_client.get(reverse_url)
                self.assertTemplateUsed(response, expected_template)
