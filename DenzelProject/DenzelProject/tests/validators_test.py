from django.core.exceptions import ValidationError
from django.test import TestCase

from DenzelProject.blogPost.models import Comment, Post
from DenzelProject.utils import CreateUserMixin, CreateObjectsTestMixin


class PhoneNumberValidatorTest(TestCase, CreateUserMixin):
    data = {
        'phone_number__with_letters': '088dasd88239023',
        'phone_number__with_plus': '+08888239023',
        'phone_number__without_plus': '08888239023',
    }

    def setUp(self) -> None:
        self.user = self._create_user(other_credentials=None)
        self.profile = self.user.profile

    def test_invalid_phone_number(self):
        self.profile.phone_number = self.data['phone_number__with_letters']

        with self.assertRaises(ValidationError) as exc:
            self.profile.full_clean()
            self.profile.save()

    def test_valid_phone_number(self):
        self.profile.phone_number = self.data['phone_number__with_plus']
        self.profile.full_clean()
        self.profile.save()

        self.profile.phone_number = self.data['phone_number__without_plus']
        self.profile.full_clean()
        self.profile.save()


class MinValidatorTest(TestCase, CreateUserMixin):
    data = {
        'first_name__below_limit': 'ab',
        'first_name__on_the_limit': 'abc',
        'first_name__above_limit': 'abcd',
    }

    def setUp(self) -> None:
        self.user = self._create_user(other_credentials=None)
        self.profile = self.user.profile

    def test_below_limit__expect_to_fail(self):
        with self.assertRaises(ValidationError) as exc:
            self.profile.first_name = self.data['first_name__below_limit']
            self.profile.full_clean()
            self.profile.save()

    def test_above_limit__expect_to_pass(self):
        self.profile.first_name = self.data['first_name__above_limit']
        self.profile.full_clean()
        self.profile.save()

    def test_on_the_limit(self):
        self.profile.first_name = self.data['first_name__on_the_limit']
        self.profile.full_clean()
        self.profile.save()


class MaxValidatorTest(TestCase, CreateUserMixin, CreateObjectsTestMixin):
    data = {
        'content__below_limit': 'abcd',
        'content__on_the_limit': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin mattis a lectus sed tempor. Aliquam placerat lacinia egestas. Curabitur sed sem sem. Mauris et orci vel ante feugiat luctus id a neque. Vivamus suscipit diam et lacus pulvinar convallis. Cras placerat nisl at justo placerat, ut placerat.',
        'content__above_limit': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam porttitor finibus tellus, in sodales orci dictum a. Sed interdum scelerisque dolor, eu laoreet purus posuere id. Nulla suscipit et sapien vel pulvinar. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos metus.',
    }

    def setUp(self) -> None:
        self.user = self._create_user(other_credentials=None)
        self.post = Post.objects.create(
            header='test_post',
            owner=self.user
        )
        self._create_objects(Comment, self.user, self.post, 1)
        self.comment = Comment.objects.first()

    def test_below_limit__expect_to_pass(self):
        self.comment.content = self.data['content__below_limit']
        self.comment.full_clean()
        self.comment.save()

    def test_above_limit__expect_to_fail(self):
        with self.assertRaises(ValidationError):
            self.comment.content = self.data['content__above_limit']
            self.comment.full_clean()
            self.comment.save()

    def test_on_the_limit(self):
        print(len(self.data['content__on_the_limit']))
        self.comment.content = self.data['content__on_the_limit']
        self.comment.full_clean()
        self.comment.save()


class File:
    size = 0

    def set_size(self, limit):
        self.size = limit


class Image:
    _committed = True
    file = File()


class MaxSizeValidatorTest(TestCase, CreateUserMixin):
    data = {
        'photo__below_limit': 1 * 1024 * 1024,
        'photo__on_the_limit': 2 * 1024 * 1024,
        'photo__above_limit': 3 * 1024 * 1024,
    }

    def setUp(self) -> None:
        self.user = self._create_user(other_credentials=None)
        self.post = Post.objects.create(
            header='test_post',
            owner=self.user
        )

    def test_below_limit__expect_to_pass(self):
        File.set_size(File, self.data['photo__below_limit'])
        self.post.image = Image()
        self.post.full_clean()
        self.post.save()

    def test_above_limit__expect_to_fail(self):
        with self.assertRaises(ValidationError):
            File.set_size(File, self.data['photo__above_limit'])
            self.post.image = Image()
            self.post.full_clean()
            self.post.save()

    def test_on_the_limit(self):
        File.set_size(File, self.data['photo__on_the_limit'])
        self.post.image = Image()
        self.post.full_clean()
        self.post.save()
