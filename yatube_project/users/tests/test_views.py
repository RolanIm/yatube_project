from django.contrib.auth.forms import UsernameField
from django.urls import reverse
from django import forms
from .fixtures import TestUsers


class ViewsTestsUsers(TestUsers):
    def test_reverse_use_correct_templates(self):
        reverse_and_templates = {
            reverse('users:signup'): 'users/signup.html',
            reverse('users:logout'): 'users/logged_out.html',
            reverse('users:login'): 'users/login.html',
            reverse('users:password_reset'): 'users/password_reset_form.html',
            reverse('users:password_reset_done'): (
                'users/password_reset_done.html'
            ),
            reverse('users:password_reset_confirm',
                    kwargs={'uidb64': 'Mg', 'token': '6dj-acc317471525c3452e33'}
                    ): 'users/password_reset_confirm.html',
            reverse('users:password_reset_complete'): (
                'users/password_reset_complete.html'
            ),
        }
        for reverse_url, expected_template in reverse_and_templates.items():
            with self.subTest(reverse_name=reverse_url):
                response = self.auth_client.get(reverse_url)
                self.assertTemplateUsed(response, expected_template)

    def test_correct_signup_view_context(self):
        response = self.auth_client.get(reverse('users:signup'))
        form_fields = {
            'first_name': forms.CharField,
            'last_name': forms.CharField,
            'username': UsernameField,
            'email': forms.EmailField
        }
        for field, expected_type in form_fields.items():
            with self.subTest(field_name=field):
                form_field = response.context['form'].fields[field]
                self.assertIsInstance(form_field, expected_type)
