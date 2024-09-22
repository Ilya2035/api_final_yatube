"""Базовые Viewsets."""

from rest_framework import viewsets, permissions, filters
from rest_framework.mixins import ListModelMixin, CreateModelMixin


class BaseFollowViewSet(viewsets.GenericViewSet,
                        ListModelMixin,
                        CreateModelMixin):
    """Базовый вьюсет для подписок."""

    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['following__username']

    def get_queryset(self):
        """Возвращает подписки текущего пользователя."""
        return self.request.user.follows.all()

    def perform_create(self, serializer):
        """Передает текущего пользователя в сериализатор при создании."""
        serializer.save(user=self.request.user)
