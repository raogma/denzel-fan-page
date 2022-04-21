from django.test import TestCase
from django.urls import reverse_lazy, reverse

from DenzelProject.blogPost.models import Post
from DenzelProject.utils import CreateUserMixin


class CreatePostTest(TestCase, CreateUserMixin):
    def setUp(self) -> None:
        self.user = self._create_user(other_credentials=None)
        self.client.login(**self.user_credentials)

    def test_correct_template_used(self):
        view = self.client.get(reverse_lazy('create-post'))
        self.assertTemplateUsed(view, 'posts/create-post.html')

    def test_not_logged_in__should_redirect(self):
        self.client.logout()
        view = self.client.get(reverse_lazy('create-post'))
        self.assertRedirects(view, '/profile/login/?next=/posts/create/')

    def test_userfield_added_to_post_after_creation(self):
        response = self.client.post(
            reverse_lazy('create-post'),
            data={
                'header': 'test_post'
            }
        )
        self.assertRedirects(response, reverse_lazy('posts'))

        post = Post.objects.first()
        self.assertIsNotNone(post.owner_id)


class EditPostTest(TestCase, CreateUserMixin):
    def setUp(self) -> None:
        self.user = self._create_user(other_credentials=None)
        self.client.login(**self.user_credentials)
        self.post = Post.objects.create(
            header='test_post',
            owner=self.user
        )

    def test_correct_template_used(self):
        view = self.client.get(reverse_lazy('edit-post', kwargs={'pk': self.post.pk}))
        self.assertTemplateUsed(view, 'posts/edit-post.html')

    def test_not_logged_in__should_redirect(self):
        self.client.logout()
        view = self.client.get(reverse_lazy('edit-post', kwargs={'pk': self.post.pk}))
        self.assertRedirects(view, f'/profile/login/?next=/posts/edit/{self.post.pk}')

    def test_redirect_after_edit__and_correct_post_data(self):
        response = self.client.post(
            reverse_lazy('edit-post', kwargs={'pk': self.post.pk}),
            data={
                'header': 'test_post_edited',
                'description': 'added description'
            }
        )
        self.assertRedirects(response, reverse_lazy('post-details', kwargs={'pk': self.post.pk}))

        post = Post.objects.first()
        self.assertEqual(post.header, 'test_post_edited')
        self.assertEqual(post.description, 'added description')


class DeletePostTest(TestCase, CreateUserMixin):
    def setUp(self) -> None:
        self.user = self._create_user(other_credentials=None)
        self.client.login(**self.user_credentials)
        self.post = Post.objects.create(
            header='test_post',
            owner=self.user
        )

    def test_correct_template_used(self):
        view = self.client.get(reverse_lazy('delete-post', kwargs={'pk': self.post.pk}))
        self.assertTemplateUsed(view, 'posts/delete-post.html')

    def test_not_logged_in__should_redirect(self):
        self.client.logout()
        view = self.client.get(reverse_lazy('delete-post', kwargs={'pk': self.post.pk}))
        self.assertRedirects(view, f'/profile/login/?next=/posts/delete/{self.post.pk}')

    def test_redirect_after_delete__and_correct_post_data(self):
        response = self.client.post(
            reverse_lazy('delete-post', kwargs={'pk': self.post.pk})
        )
        self.assertRedirects(response, reverse_lazy('posts'))

        post = Post.objects.first()
        self.assertIsNone(post)

