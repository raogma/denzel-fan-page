from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy
from DenzelProject.blogPost.models import Post, Like, Dislike
from DenzelProject.utils import CreateUserMixin


class CreateUserTest(TestCase, CreateUserMixin):
    other_user_credentials = {
        'email': 'other@gmail.com',
        'password': '1234'
    }
    def _get_response(self, user_obj):
        return self.client.get(reverse_lazy('profile-details', kwargs={'pk': user_obj.pk}))
    def _create_and_users__log_other_user(self):
        user_obj = self._create_user(self.user_credentials)
        other_user_obj = self._create_user(self.other_user_credentials)
        self.client.login(**self.other_user_credentials)
        return user_obj, other_user_obj
    @staticmethod
    def _create_user(credentials):
        user = get_user_model()
        user_obj = user.objects.create_user(**credentials)
        return user_obj
    @staticmethod
    def _create_liking(action, owner, posts_ids):
        if action == 'like':
            for x in posts_ids:
                Like.objects.create(
                    post_id=x,
                    owner=owner,
                )
        else:
            for x in posts_ids:
                Dislike.objects.create(
                    post_id=x,
                    owner=owner,
                )
    @staticmethod
    def _create_posts(total, owner):
        for x in range(total):
            Post.objects.create(
                header=f'test_post_{x}',
                owner=owner
            )
    def test_user_posts_correct_count(self):
        user_obj = self._create_user(self.user_credentials)
        self.client.login(**self.user_credentials)
        self._create_posts(3, user_obj)
        response = self._get_response(user_obj)
        user_posts = response.context['user_posts']
        self.assertEqual(len(user_posts), 3)
    def test_filter_of_posts__only_profile_posts(self):
        user_obj, other_user_obj = self._create_and_users__log_other_user()
        self._create_posts(2, other_user_obj)
        self.client.logout()
        self.client.login(**self.user_credentials)
        self._create_posts(3, user_obj)
        response = self._get_response(user_obj)
        user_posts = response.context['user_posts']
        self.assertEqual(len(user_posts), 3)
    def test_user_has_no_posts__equals_zero__despite_other_users_posts(self):
        user_obj, other_user_obj = self._create_and_users__log_other_user()
        self._create_posts(2, other_user_obj)
        self.client.logout()
        self.client.login(**self.user_credentials)
        response = self._get_response(user_obj)
        user_posts = response.context['user_posts']
        self.assertEqual(len(user_posts), 0)
    def test_zero_liking__not_raise_division_by_zero_error(self):
        user_obj = self._create_user(self.user_credentials)
        self.client.login(**self.user_credentials)
        response = self._get_response(user_obj)
        self.assertEqual(response.context['liking_percent'], 0)
    def test_more_likes__show_correct_percent_like_progress_bar(self):
        user_obj = self._create_user(self.user_credentials)
        self.client.login(**self.user_credentials)
        self._create_posts(11, user_obj)
        self._create_liking('like', user_obj, [x for x in range(1, 10)])
        self._create_liking('dislike', user_obj, [10,])
        response = self._get_response(user_obj)
        self.assertEqual(response.context['liking_percent'], 90)
    def test_more_dislikes__show_correct_percent_like_progress_bar(self):
        user_obj = self._create_user(self.user_credentials)
        self.client.login(**self.user_credentials)
        self._create_posts(11, user_obj)
        self._create_liking('like', user_obj, [10,])
        self._create_liking('dislike', user_obj, [x for x in range(1, 10)])
        response = self._get_response(user_obj)
        self.assertEqual(response.context['liking_percent'], 10)
    def test_view__if_user_authenticated(self):
        user = get_user_model()
        user_obj = user.objects.create_user(**self.user_credentials)
        self.client.login(**self.user_credentials)
        response = self._get_response(user_obj)
        self.assertTemplateUsed(response, 'profile/profile-details.html')
    def test_view_redirect_user_to_login__if_user_not_authenticated(self):
        response = self.client.get('/profile/details/1/')
        self.assertRedirects(response, '/profile/login/?next=/profile/details/1/')