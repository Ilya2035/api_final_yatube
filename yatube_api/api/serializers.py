"""Модуль, содержащий сериализаторы для моделей API."""

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.contrib.auth import get_user_model

from posts.models import Comment, Post, Group, Follow
from rest_framework.validators import UniqueTogetherValidator

User = get_user_model()

"""
flake8 не пропускает если удалить, может я что то не так понял?
плюс в прошлый раз вы не указали это.
"""


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Post."""

    author = SlugRelatedField(slug_field='username', read_only=True)
    image = serializers.ImageField(required=False)
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        required=False
    )

    class Meta:
        """Мета-класс для модели Post."""

        model = Post
        fields = ('id', 'text', 'author', 'image', 'group', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        """Мета-класс для модели Comment."""

        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('post',)


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Group."""

    class Meta:
        """Мета-класс для модели Group."""

        model = Group
        fields = ('id', 'title', 'slug', 'description')


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Follow."""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user_username = serializers.ReadOnlyField(source='user.username')
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        """Мета-класс для модели Follow."""

        model = Follow
        fields = ('user', 'user_username', 'following')
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'],
                message="Вы уже подписаны на этого пользователя."
            )
        ]

    def validate_following(self, value):
        """
        Field-level валидация для поля 'following'.

        Проверяет, что пользователь не подписывается на самого себя.
        """
        user = self.context['request'].user
        if value == user:
            raise serializers.ValidationError(
                "Нельзя подписаться на самого себя.")
        return value

    def to_representation(self, instance):
        """
        Переопределяет метод представления объекта.

        Включает поле 'user_username' для отображения имени пользователя.
        """
        representation = super().to_representation(instance)
        representation['user'] = representation.pop('user_username')
        return representation


"""
тяжело, не могу понять правильно ли я сделал.
В конце я добавил to_representation, но не уверен правильно ли это и как
можно сделать по другому.
"""
