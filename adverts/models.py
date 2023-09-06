from django.contrib.auth.models import User
from django.db import models


CATEGORIES = [
    ('TA', 'Танки'),
    ('HL', 'Хилы'),
    ('DD', 'ДД'),
    ('TR', 'Торговцы'),
    ('GM', 'Гилдмастеры'),
    ('QG', 'Квестгиверы'),
    ('SM', 'Кузнецы'),
    ('TN', 'Кожевники'),
    ('PT', 'Зельевары'),
    ('SP', 'Мастера заклинаний'),
]


class Post(models.Model):

    date_of_creation = models.DateTimeField(
        auto_now_add=True,
    )

    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='post_created_by',
    )

    title = models.CharField(
        max_length=255,
        help_text='Up to 255 symbols',
    )

    category = models.CharField(
        max_length=15,
        choices=CATEGORIES,
        default=None,
    )

    content = models.TextField(
        blank=True,
    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self) -> str:
        return f'{self.title}'


class Reply(models.Model):

    date_of_creation = models.DateTimeField(
        auto_now_add=True,
    )

    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='reply_created_by',
    )

    adv = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='replies_to_post',
    )

    text = models.TextField(
        blank=True,
    )

    is_approved = models.BooleanField(
        default=False,
    )

    is_rejected = models.BooleanField(
        default=False,
    )

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self) -> str:
        return f'{self.text[:50]}...'

    def approve(self) -> None:
        self.is_approved = True
        self.save()

    def disapprove(self) -> None:
        self.is_approved = False
        self.save()

    def reject(self) -> None:
        self.is_rejected = True
        self.save()

    def unreject(self) -> None:
        self.is_rejected = False
        self.save()