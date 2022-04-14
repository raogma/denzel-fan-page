from django.test import TestCase
from django.urls import reverse_lazy

from DenzelProject.utils import CreateUserMixin


class LoginTest(TestCase, CreateUserMixin):
    def test_template(self):
        self.assertTemplateUsed('profile/login.html')

    def test_correct_redirect_after_success(self):
        self._create_user(other_credentials=None)
        response = self.client.post(
            reverse_lazy('login'),
            data={
                'username': self.user_credentials['email'],
                'password': self.user_credentials['password']
            }
        )
        self.assertRedirects(response, reverse_lazy('posts'))


class LogoutTemplateTest(TestCase):
    def test_correct_template(self):
        self.assertTemplateUsed('profile/logout.html')

    def test_not_authenticated_access__redirect_to_login(self):
        response = self.client.get(
            reverse_lazy('logout')
        )
        self.assertRedirects(response, '/profile/login/?next=/profile/logout/')


class LogoutConfirmTest(TestCase, CreateUserMixin):
    def test_correct_redirect_after_success(self):
        self._create_user(other_credentials=None)
        self.client.login(**self.user_credentials)
        response = self.client.post(
            reverse_lazy('logout-confirm'),
            data={}
        )
        self.assertRedirects(response, reverse_lazy('welcome'))

    def test_not_authenticated_access__redirect_to_login(self):
        response = self.client.get(
            reverse_lazy('logout-confirm')
        )
        self.assertRedirects(response, '/profile/login/?next=/profile/logout-confirm/')
