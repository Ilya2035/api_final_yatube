"""Модуль, содержащий view-классы для API."""

from rest_framework import viewsets, permissions, filters
from rest_framework.exceptions import ValidationError
from .serializers import (GroupSerializer, FollowSerializer,
                          PostSerializer, CommentSerializer)
from .permissions import IsAuthorOrReadOnly, OptionalLimitOffsetPagination

from posts.models import Group, Follow, Post, Comment


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Предоставляет действия `list` и `retrieve` для модели Group."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class AllGroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Предоставляет действия для всех групп с фильтрацией."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']


class FollowViewSet(viewsets.GenericViewSet,
                    viewsets.mixins.ListModelMixin,
                    viewsets.mixins.CreateModelMixin):
    """Представление для подписок, реализующее создание и просмотр."""

    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['following__username']
    pagination_class = None

    def get_queryset(self):
        """Возвращает подписки текущего пользователя."""
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Создает подписку для текущего пользователя."""
        user = self.request.user
        following = serializer.validated_data.get('following')

        if Follow.objects.filter(user=user, following=following).exists():
            raise ValidationError('Вы уже подписаны на этого пользователя.')

        serializer.save(user=user)


class PostViewSet(viewsets.ModelViewSet):
    """Представление для CRUD операций с публикациями."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly
    ]
    pagination_class = OptionalLimitOffsetPagination

    def perform_create(self, serializer):
        """Создает публикацию от имени текущего пользователя."""
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Представление для CRUD операций с комментариями."""

    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly
    ]
    pagination_class = None

    def get_queryset(self):
        """Возвращает комментарии для конкретной публикации."""
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post__id=post_id)

    def perform_create(self, serializer):
        """Создает комментарий к публикации."""
        post_id = self.kwargs.get('post_id')
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise ValidationError("Публикация не найдена.")
        serializer.save(author=self.request.user, post=post)
