"""Модуль, содержащий классы разрешений и пагинации для API приложения."""

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    """Разрешение для автора; остальным доступно чтение."""

    def has_object_permission(self, request, view, obj):
        """Проверяет права на изменение объекта."""
        return request.method in SAFE_METHODS or obj.author == request.user
