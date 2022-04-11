from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy


class WelcomeViewTest(TestCase):
    user_credentials = {
        'email': 'r.marinkov99@gmail.com',
        'password': '1234'
    }

    def test_welcome_view__if_user_not_authenticated(self):
        response = self.client.get(reverse_lazy('welcome'))
        self.assertTemplateUsed(response, 'welcome.html')

    def test_welcome_view_redirect_user_to_posts__if_user_authenticated(self):
        user = get_user_model()
        user.objects.create_user(**self.user_credentials)
        self.client.login(**self.user_credentials)

        response = self.client.get(reverse_lazy('welcome'))
        self.assertRedirects(response, reverse_lazy('posts'))


class ContactsViewTest(TestCase):
    user_credentials = {
        'email': 'r.marinkov99@gmail.com',
        'password': '1234'
    }

    def test_contacts_view__if_user_authenticated(self):
        user = get_user_model()
        user.objects.create_user(**self.user_credentials)
        self.client.login(**self.user_credentials)

        response = self.client.get(reverse_lazy('contacts'))
        self.assertTemplateUsed(response, 'contacts.html')

    def test_contacts_view_redirect_user_to_login__if_user_not_authenticated(self):
        response = self.client.get(reverse_lazy('contacts'))
        self.assertRedirects(response, '/profile/login/?next=/contacts/')  # # ??
