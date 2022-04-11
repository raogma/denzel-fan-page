from django.contrib.auth import get_user_model
from django.urls import reverse


class ProfileMixin:
    user_credentials = {
        'email': 'test@gmail.com',
        'password': '1234',
    }

    def _create_user(self, other_credentials):
        credentials = self.user_credentials
        if other_credentials:
            credentials = other_credentials
        user = get_user_model().objects.create_user(**credentials)
        return user
