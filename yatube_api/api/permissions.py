"""Модуль, содержащий классы разрешений и пагинации для API приложения."""

from rest_framework import permissions
from rest_framework.pagination import LimitOffsetPagination


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Разрешение для автора; остальным доступно чтение."""

    def has_object_permission(self, request, view, obj):
        """Проверяет права на изменение объекта."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class OptionalLimitOffsetPagination(LimitOffsetPagination):
    """Пагинация для параметров limit и offset."""

    def paginate_queryset(self, queryset, request, view=None):
        """Пагинирует queryset по limit или offset."""
        if 'limit' in request.query_params or 'offset' in request.query_params:
            return super().paginate_queryset(queryset, request, view)
        return None
