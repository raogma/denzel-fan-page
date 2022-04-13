from django.test import TestCase
from django.urls import reverse_lazy

from DenzelProject.blogPost.models import Post, Like, Dislike
from DenzelProject.utils import ProfileTestMixin


class DashTest(TestCase):
    def test_public_access(self):
        response = self.client.get(reverse_lazy('posts'))
        self.assertTemplateUsed(response, 'dashboard.html')


class LikingTest(TestCase, ProfileTestMixin):
    def setUp(self) -> None:
        self.user = self._create_user(other_credentials=None)
        self.client.login(**self.user_credentials)
        self.post = Post.objects.create(
            header='test_post',
            owner=self.user,
        )

    def test_like_post__should_increment__and_redirect_to_same_page(self):
        response = self.client.get(reverse_lazy('post-details-like', kwargs={'pk': self.post.pk}))
        searched_like = Like.objects.filter(
            owner=self.user,
            post=self.post
        )
        self.assertEqual(len(searched_like), 1)
        self.assertRedirects(response, reverse_lazy('post-details', kwargs={'pk': self.post.pk}))

    def test_dislike_post__should_increment__and_redirect_to_same_page(self):
        response = self.client.get(reverse_lazy('post-details-dislike', kwargs={'pk': self.post.pk}))
        searched_dislike = Dislike.objects.filter(
            owner=self.user,
            post=self.post
        )
        self.assertEqual(len(searched_dislike), 1)
        self.assertRedirects(response, reverse_lazy('post-details', kwargs={'pk': self.post.pk}))

    def test_liked_post__dislike_should_remove_like(self):
        self.client.get(reverse_lazy('post-details-like', kwargs={'pk': self.post.pk}))
        self.client.get(reverse_lazy('post-details-dislike', kwargs={'pk': self.post.pk}))

        searched_like = Like.objects.filter(
            owner=self.user,
            post=self.post
        )

        searched_dislike = Dislike.objects.filter(
            owner=self.user,
            post=self.post
        )

        self.assertEqual(len(searched_like), 0)
        self.assertEqual(len(searched_dislike), 1)

    def test_disliked_post__like_should_remove_dislike(self):
        self.client.get(reverse_lazy('post-details-dislike', kwargs={'pk': self.post.pk}))
        self.client.get(reverse_lazy('post-details-like', kwargs={'pk': self.post.pk}))

        searched_like = Like.objects.filter(
            owner=self.user,
            post=self.post
        )

        searched_dislike = Dislike.objects.filter(
            owner=self.user,
            post=self.post
        )

        self.assertEqual(len(searched_like), 1)
        self.assertEqual(len(searched_dislike), 0)

    def test_disliked_post__like_should_remove_dislike(self):
        self.client.get(reverse_lazy('post-details-dislike', kwargs={'pk': self.post.pk}))
        self.client.get(reverse_lazy('post-details-like', kwargs={'pk': self.post.pk}))

        searched_like = Like.objects.filter(
            owner=self.user,
            post=self.post
        )

        searched_dislike = Dislike.objects.filter(
            owner=self.user,
            post=self.post
        )

        self.assertEqual(len(searched_like), 1)
        self.assertEqual(len(searched_dislike), 0)

    def test_liked_post__like_should_remove_like(self):
        self.client.get(reverse_lazy('post-details-like', kwargs={'pk': self.post.pk}))
        self.client.get(reverse_lazy('post-details-like', kwargs={'pk': self.post.pk}))

        searched_like = Like.objects.filter(
            owner=self.user,
            post=self.post
        )
        self.assertEqual(len(searched_like), 0)

    def test_disliked_post__dislike_should_remove_dislike(self):
        self.client.get(reverse_lazy('post-details-dislike', kwargs={'pk': self.post.pk}))
        self.client.get(reverse_lazy('post-details-dislike', kwargs={'pk': self.post.pk}))

        searched_dislike = Dislike.objects.filter(
            owner=self.user,
            post=self.post
        )
        self.assertEqual(len(searched_dislike), 0)
