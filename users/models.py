from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from nullable import NULLABLE
from users.management.email_user_manager import EmailUserManager

ROLE_CHOICES = (
    ("user", "User"),
    ("admin", "Admin"),
)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, help_text="Укажите вашу почту")
    first_name = models.CharField(
        max_length=30,
        help_text="Укажите ваше имя"
    )
    last_name = models.CharField(
        max_length=30,
        help_text="Укажите вашу фамилию"
    )
    phone = PhoneNumberField(
        verbose_name="Телефон",
        **NULLABLE,
        help_text="Введите номер телефона"
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        verbose_name="Аватар",
        **NULLABLE,
        help_text="Загрузите изображение",
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="user")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = EmailUserManager()

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
