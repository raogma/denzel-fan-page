from django.test import TestCase
from django.urls import reverse_lazy

from DenzelProject.blogPost.models import Post, Comment
from DenzelProject.utils import ProfileTestMixin, CreateObjectsTestMixin


class CommentCreateTest(TestCase, ProfileTestMixin, CreateObjectsTestMixin):
    def setUp(self) -> None:
        self.user = self._create_user(other_credentials=None)
        self.client.login(**self.user_credentials)
        self.post = Post.objects.create(
            header='test_post',
            owner=self.user
        )
        self.view = self.client.get(reverse_lazy(
            'post-details-comments',
            kwargs={
                'pk': self.post.pk,
                'page': 1,
            }))

    def test_not_logged_in__should_redirect(self):
        self.client.logout()
        view = self.client.get(reverse_lazy(
            'post-details-comments',
            kwargs={
                'pk': self.post.pk,
                'page': 1,
            }))
        self.assertRedirects(view, f'/profile/login/?next=/posts/details/{self.post.pk}/comments/create/page/1/')

    def test_correct_template_used(self):
        self.assertTemplateUsed(self.view, 'posts/comments.html')

    def test_add_owner_and_post_to_comment__after_creation(self):
        view = self.client.post(
            reverse_lazy(
                'post-details-comments',
                kwargs={
                    'pk': self.post.pk,
                    'page': 1,
                }
            ),
            data={
                'content': 'comment_example',
            }
        )
        comment = Comment.objects.first()
        self.assertEqual(comment.owner, self.user)
        self.assertEqual(comment.post, self.post)

    def test_context__related_to_post_only_comments_show(self):
        other_post = Post.objects.create(
            header='other_post',
            owner=self.user,
        )
        self._create_objects(Comment, self.user, self.post, 3)
        self._create_objects(Comment, self.user, other_post, 2)

        view = self.client.get(reverse_lazy(
            'post-details-comments',
            kwargs={
                'pk': self.post.pk,
                'page': 1,
            }
        ))
        comments = view.context['object_list']
        self.assertEqual(len(comments), 3)


class CommentDeleteTest(TestCase, ProfileTestMixin, CreateObjectsTestMixin):
    def setUp(self) -> None:
        self.user = self._create_user(other_credentials=None)
        self.client.login(**self.user_credentials)
        self.post = Post.objects.create(
            header='test_post',
            owner=self.user
        )
        self.comment = Comment.objects.create(
            content='comment_example',
            owner=self.user,
            post=self.post,
        )
        self.view = self.client.get(reverse_lazy(
            'post-delete-comments',
            kwargs={
                'pk': self.post.pk,
                'comment': self.comment.pk,
                'page': 1,
            }
        ))

    def test_not_logged_in__should_redirect(self):
        self.client.logout()
        view = self.client.get(reverse_lazy(
            'post-delete-comments',
            kwargs={
                'pk': self.post.pk,
                'comment': self.comment.pk,
                'page': 1,
            }
        ))
        self.assertRedirects(
            view, f'/profile/login/?next=/posts/details/{self.post.pk}/comments/delete/{self.comment.pk}/page/1'
        )

    def test_correct_template_used(self):
        self.assertTemplateUsed(self.view, 'posts/comments.html')

    def test_comment_existence__after_removal(self):
        view = self.client.post(
            reverse_lazy(
                'post-delete-comments',
                kwargs={
                    'pk': self.post.pk,
                    'comment': self.comment.pk,
                    'page': 1,
                }
            ),
            data={
                'content': self.comment.content
            }
        )
        comment = Comment.objects.first()
        self.assertIsNone(comment)


class CommentEditTest(TestCase, ProfileTestMixin, CreateObjectsTestMixin):
    def setUp(self) -> None:
        self.user = self._create_user(other_credentials=None)
        self.client.login(**self.user_credentials)
        self.post = Post.objects.create(
            header='test_post',
            owner=self.user
        )
        self.comment = Comment.objects.create(
            content='comment_example',
            owner=self.user,
            post=self.post,
        )
        self.view = self.client.get(reverse_lazy(
            'post-edit-comments',
            kwargs={
                'pk': self.post.pk,
                'comment': self.comment.pk,
                'page': 1,
            }
        ))

    def test_not_logged_in__should_redirect(self):
        self.client.logout()
        view = self.client.get(reverse_lazy(
            'post-edit-comments',
            kwargs={
                'pk': self.post.pk,
                'comment': self.comment.pk,
                'page': 1,
            }
        ))
        self.assertRedirects(
            view, f'/profile/login/?next=/posts/details/{self.post.pk}/comments/edit/{self.comment.pk}/page/1'
        )

    def test_correct_template_used(self):
        self.assertTemplateUsed(self.view, 'posts/comments.html')

    def test_comment_existence__after_edit(self):
        view = self.client.post(
            reverse_lazy(
                'post-edit-comments',
                kwargs={
                    'pk': self.post.pk,
                    'comment': self.comment.pk,
                    'page': 1,
                }
            ),
            data={
                'content': 'edited_comment'
            }
        )
        comment = Comment.objects.first()
        self.assertEqual(comment.content, 'edited_comment')
