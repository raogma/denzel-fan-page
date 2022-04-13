from django.test import TestCase
from django.urls import reverse_lazy

from DenzelProject.blogPost.models import Post, Like, Dislike, Comment
from DenzelProject.utils import ProfileTestMixin, CreateObjectsTestMixin


class PostDetailsTest(TestCase, ProfileTestMixin, CreateObjectsTestMixin):
    test1_credentials = {
        'email': 'test1@gmail.com',
        'password': '1234',
    }
    test2_credentials = {
        'email': 'test2@gmail.com',
        'password': '1234',
    }

    def setUp(self) -> None:
        self.user = self._create_user(other_credentials=None)
        self.client.login(**self.user_credentials)
        self.post = Post.objects.create(
            header='test_post',
            owner=self.user,
        )

    def test_corrent_count_likes__in_context(self):
        user1 = self._create_user(self.test1_credentials)
        user2 = self._create_user(self.test2_credentials)
        self._create_objects(Like, self.user, self.post, 1)
        self._create_objects(Like, user1, self.post, 1)
        self._create_objects(Like, user2, self.post, 1)

        response = self.client.get(reverse_lazy('post-details', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.context['likes_count'], 3)

    def test_corrent_count_dislikes__in_context(self):
        user1 = self._create_user(self.test1_credentials)
        user2 = self._create_user(self.test2_credentials)
        self._create_objects(Dislike, self.user, self.post, 1)
        self._create_objects(Dislike, user1, self.post, 1)
        self._create_objects(Dislike, user2, self.post, 1)

        response = self.client.get(reverse_lazy('post-details', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.context['dislikes_count'], 3)

    def test_corrent_count_comments__in_context(self):
        self._create_objects(Comment, self.user, self.post, 3)
        response = self.client.get(reverse_lazy('post-details', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.context['comments_count'], 3)

    def test_corrent_owner__in_context(self):
        response = self.client.get(reverse_lazy('post-details', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.context['owner'], self.user.profile)

    def test_correct_template_used(self):
        response = self.client.get(reverse_lazy('post-details', kwargs={'pk': self.post.pk}))
        self.assertTemplateUsed(response, 'posts/post-details.html')
