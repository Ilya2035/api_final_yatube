"""Базовые Viewsets."""

from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, CreateModelMixin


class CreateListViewSet(
    viewsets.GenericViewSet,
    ListModelMixin,
    CreateModelMixin
):
    """
    Базовый ViewSet, предоставляет `list` (список) и `create` (создание).

    Необходимо переопределить его и задать атрибуты `.queryset`
    и `.serializer_class`. Этот класс можно использовать для создания
    общих поведений, которые будут переиспользоваться в других
    ViewSet-классах API.
    """

    pass
