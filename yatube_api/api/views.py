"""Модуль, содержащий view-классы для API."""

from rest_framework import viewsets, permissions, filters
from django.shortcuts import get_object_or_404

from .serializers import (GroupSerializer, FollowSerializer,
                          PostSerializer, CommentSerializer)
from .viewsets import BasePostCommentViewSet

from posts.models import Group, Post


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Предоставляет действия `list` и `retrieve` для модели Group."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.AllowAny]


class FollowViewSet(viewsets.GenericViewSet,
                    viewsets.mixins.ListModelMixin,
                    viewsets.mixins.CreateModelMixin):
    """Представление для подписок, реализующее создание и просмотр."""

    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['following__username']

    def get_queryset(self):
        """Возвращает подписки текущего пользователя."""
        return self.request.user.follows.all()


class PostViewSet(BasePostCommentViewSet):
    """Представление для CRUD операций с публикациями."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(BasePostCommentViewSet):
    """Представление для CRUD операций с комментариями."""

    serializer_class = CommentSerializer

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
