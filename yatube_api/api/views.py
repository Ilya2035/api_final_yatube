"""Модуль, содержащий view-классы для API."""

from rest_framework import viewsets, permissions
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404

from .permissions import IsAuthorOrReadOnly
from .serializers import (GroupSerializer, FollowSerializer,
                          PostSerializer, CommentSerializer)
from .viewsets import BaseFollowViewSet
from posts.models import Group, Post


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Предоставляет действия `list` и `retrieve` для модели Group."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.AllowAny]


class FollowViewSet(BaseFollowViewSet):
    """Представление для подписок, используя базовый вьюсет."""

    serializer_class = FollowSerializer


class PostViewSet(viewsets.ModelViewSet):
    """Представление для CRUD операций с публикациями."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly
    ]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Привязывает объект к текущему пользователю."""
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Представление для CRUD операций с комментариями."""

    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly
    ]

    def get_queryset(self):
        """Возвращает список комментариев для указанного поста."""
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        return post.comments.all()

    def perform_create(self, serializer):
        """Привязывает комментарий к указанному посту и автору."""
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)
