"""Базовые Viewsets."""

from rest_framework import viewsets, permissions
from .permissions import IsAuthorOrReadOnly
from .paginators import OptionalLimitOffsetPagination


class BasePostCommentViewSet(viewsets.ModelViewSet):
    """вьюсет для моделей с CRUD операциями и пользовательскими правами."""

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly
    ]
    pagination_class = OptionalLimitOffsetPagination

    def perform_create(self, serializer):
        """Привязывает объект к текущему пользователю."""
        serializer.save(author=self.request.user)
