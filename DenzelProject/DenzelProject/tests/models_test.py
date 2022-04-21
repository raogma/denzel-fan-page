from django.test import TestCase
from DenzelProject.profileApp.models import Profile
from DenzelProject.utils import CreateUserMixin


class CreateUser(TestCase, CreateUserMixin):
    names_data = {
        'first_name': 'test_name_1',
        'last_name': 'test_name_2',
    }

    def setUp(self) -> None:
        user = self._create_user(other_credentials=None)
        self.profile = Profile.objects.get(user_id=user.pk)

    def test_get_name_method__only_first_name(self):
        self.profile.first_name = self.names_data['first_name']
        self.profile.save()
        self.assertEqual(self.profile.get_name(), 'test_name_1')

    def test_get_name_method__only_last_name(self):
        self.profile.last_name = self.names_data['last_name']
        self.profile.save()
        self.assertEqual(self.profile.get_name(), 'test_name_2')

    def test_get_name_method__first_name_and_last_name(self):
        self.profile.first_name = self.names_data['first_name']
        self.profile.last_name = self.names_data['last_name']
        self.profile.save()
        self.assertEqual(self.profile.get_name(), 'test_name_1 test_name_2')

    def test_get_name_method__empty(self):
        self.assertEqual(self.profile.get_name(), 'Anonymous User')

    def test_generate_username(self):
        self.assertEqual(self.profile.generate_username(), 'test')
