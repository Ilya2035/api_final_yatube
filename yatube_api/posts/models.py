"""Модуль для описания моделей базы данных приложения posts."""

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q, F

User = get_user_model()


class Group(models.Model):
    """Модель для описания группы постов."""

    title = models.CharField(
        max_length=200,
        verbose_name='Название группы',
        help_text='Введите название группы'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Уникальный слуг',
        help_text='Укажите уникальный идентификатор для URL'
    )
    description = models.TextField(
        verbose_name='Описание группы',
        help_text='Добавьте описание группы'
    )

    def __str__(self):
        """Возвращает строковое представление модели."""
        return self.title

    class Meta:
        """Мета-данные для модели Group."""

        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Post(models.Model):
    """Модель для описания постов."""

    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts',
        verbose_name='Группа',
        help_text='Группа, к которой будет относиться пост'
    )

    def __str__(self):
        """Возвращает строковое представление модели."""
        return self.text[:15]

    class Meta:
        """Мета-данные для модели Post."""

        ordering = ['-pub_date']
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'


class Comment(models.Model):
    """Модель для описания комментариев к постам."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        """Возвращает строковое представление модели."""
        return self.text[:15]

    class Meta:
        """Мета-данные для модели Comment."""

        ordering = ['-created']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Follow(models.Model):
    """Модель для описания подписок на пользователей."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follows',
        verbose_name='Подписчик'
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers',
        verbose_name='Автор'
    )

    class Meta:
        """Мета-данные для модели Follow."""

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_user_following'
            ),
            models.CheckConstraint(
                check=~Q(user=F('following')),
                name='prevent_self_follow'
            )
        ]

    def __str__(self):
        """
        Возвращает строковое представление объекта Follow.

        :return: Строка вида "user.username follows following.username".
        """
        return f"{self.user.username} follows {self.following.username}"


"""Получается нужно только добавить доп проверку? не убирая старую"""
