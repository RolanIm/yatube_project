from django.contrib.auth.models import User
from django.urls import reverse
from .fixtures import TestUsers


class TestUsersForms(TestUsers):
    def test_correct_signup_form(self):
        user_counts = User.objects.count()
        form_data = {
            'first_name': 'test-name',
            'last_name': 'test-last-name',
            'username': 'test-username123',
            'email': 'email-User@mail.com',
            'password1': 'Password1234_!',
            'password2': 'Password1234_!'
        }
        redirect_url = reverse('posts:index')
        response = self.guest_client.post(
            reverse('users:signup'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, redirect_url)
        self.assertEqual(User.objects.count(), user_counts + 1)
        self.assertTrue(
            User.objects.filter(username='test-username123').exists()
        )
