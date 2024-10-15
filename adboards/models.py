from django.db import models

from users.models import User


class Ad(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название Товара")
    description = models.TextField(verbose_name="Описание товара")
    price = models.PositiveIntegerField(verbose_name="Стоимость товара")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Автор объявления"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания объявления"
    )

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.TextField(verbose_name="Текст отзыва")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Автор отзыва"
    )
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE,
                           verbose_name="Объявление")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания отзыва"
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Отзыв от {self.author} к объявлению {self.ad}"
