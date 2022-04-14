from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy, reverse

from DenzelProject.profileApp.models import Profile
from DenzelProject.utils import CreateUserMixin


class CreateProfileTest(TestCase):
    def test_successful_register(self):
        view = self.client.get(reverse('create-profile'))
        self.assertTemplateUsed(view, 'profile/create-profile.html')

        response = self.client.post(
            reverse('create-profile'),
            data={
                'email': 'test@gmail.com',
                'password1': '1234',
                'password2': '1234',
            }
        )
        user = get_user_model().objects.first()
        profile = Profile.objects.first()

        self.assertEqual(user.pk, 1)
        self.assertEqual(profile.pk, 1)  # tests signal create profile after user registration
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=reverse_lazy('posts'))


class EditCreateUser(TestCase, CreateUserMixin):
    def test_correct_redirect(self):
        user = self._create_user(other_credentials=None)
        self.client.login(**self.user_credentials)

        view = self.client.get(reverse('edit-profile', kwargs={'pk': user.pk}))
        self.assertTemplateUsed(view, 'profile/edit-profile.html')

        response = self.client.post(
            reverse('edit-profile', kwargs={'pk': user.pk}),
            data={}
        )
        self.assertRedirects(response, reverse_lazy('profile-details', kwargs={'pk': user.pk}))

    def test_not_authenticated_access__redirect_to_login(self):
        response = self.client.post(
            reverse('edit-profile', kwargs={'pk': 1}),
            data={}
        )
        self.assertRedirects(response, '/profile/login/?next=/profile/edit/1')

    def test_change_profile_data__after_success(self):
        user = self._create_user(other_credentials=None)
        self.client.login(**self.user_credentials)

        self.client.post(
            reverse('edit-profile', kwargs={'pk': user.pk}),
            data={
                'first_name': 'TestName1',
                'phone_number': '8888888'
            }
        )
        profile = Profile.objects.first()

        self.assertEqual(profile.first_name, 'TestName1')
        self.assertEqual(profile.phone_number, '8888888')


class DeleteCreateUser(TestCase, CreateUserMixin):
    def test_delete_profile(self):
        user = self._create_user(other_credentials=None)
        self.client.login(**self.user_credentials)
        view = self.client.get(reverse('delete-profile', kwargs={'pk': user.pk}))

        self.assertTemplateUsed(view, 'profile/delete-profile.html')

        response = self.client.post(
            reverse('delete-profile', kwargs={'pk': user.pk}),
            data={}
        )

        self.assertRedirects(response, reverse_lazy('welcome'))
        self.assertIsNone(get_user_model().objects.first())
        self.assertIsNone(Profile.objects.first())  # test profile delete signal after user delete

    def test_not_authenticated_access__redirect_to_login(self):
        response = self.client.get(
            reverse('delete-profile', kwargs={'pk': 1})
        )
        self.assertRedirects(response, '/profile/login/?next=/profile/delete/1')
