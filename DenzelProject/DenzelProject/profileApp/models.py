from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager
from cloudinary.models import CloudinaryField

from DenzelProject.validators import validate_phone_only_numbers, MinValidator, MaxSizeValidatorMB


class CustomManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, )
    is_staff = models.BooleanField(default=False, )
    date_joined = models.DateTimeField(auto_now_add=True, )
    USERNAME_FIELD = 'email'
    objects = CustomManager()


class Profile(models.Model):
    gender_choices = [
        'male', 'female', 'do not show',
    ]
    avatar = CloudinaryField(
        # validators=(
        #     MaxSizeValidatorMB(2),
        # ),
        null=True,
        blank=True,
    )
    first_name = models.CharField(
        validators=(
            MinValidator(3),
        ),
        max_length=30,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        validators=(
            MinValidator(3),
        ),
        max_length=30,
        null=True,
        blank=True,
    )
    phone_number = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        validators=(
            validate_phone_only_numbers,
            MinValidator(5),
        )
    )
    address = models.CharField(
        validators=(
            MinValidator(3),
        ),
        max_length=100,
        null=True,
        blank=True,
    )
    gender = models.CharField(
        max_length=max([len(x) for x in gender_choices]),
        choices=[(x, x) for x in gender_choices],
        null=True,
        blank=True,
    )
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def get_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            return 'Anonymous User'

    def generate_username(self):
        return self.user.email.split('@')[0]
