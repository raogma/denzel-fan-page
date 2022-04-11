import os

from django.contrib.auth import get_user_model
from django.db import models

from DenzelProject.validators import MinValidator, MaxValidator, MaxSizeValidatorMB


class Post(models.Model):
    image = models.ImageField(
        validators=(
            MaxSizeValidatorMB(2),
        ),
        null=True,
        blank=True,
    )
    header = models.CharField(
        validators=(
            MinValidator(3),
        ),
        max_length=30,
    )
    description = models.TextField(
        validators=(
            MinValidator(3),
        ),
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )

    @property
    def generate_username(self):
        return self.owner.email.split('@')[0]

    def __str__(self):
        return self.header


class Comment(models.Model):
    content = models.TextField(
        validators=(
            MinValidator(3),
            MaxValidator(300),
        ),
        verbose_name='New message'
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )


class Like(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = (
            'post', 'owner'
        )


class Dislike(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = (
            'post', 'owner'
        )
