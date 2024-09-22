"""Модуль, содержащий классы пагинации для API приложения."""

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class OptionalLimitOffsetPagination(LimitOffsetPagination):
    """
    Пагинация, только при наличии параметров 'limit' или 'offset'.

    Этот класс наследует LimitOffsetPagination и переопределяет метод
    `get_paginated_response`, чтобы возвращать пагинированный
    ответ только при наличии соответствующих параметров запроса.
    В противном случае возвращает полный набор данных без пагинации.
    """

    def get_paginated_response(self, data):
        """
        Возвращает пагинированный ответ, если есть 'limit' или 'offset'.

        В противном случае возвращает полный набор данных.

        :param data: Данные для ответа.
        :return: Пагинированный или полный HTTP-ответ.
        """
        if (
            'limit' in self.request.query_params
            or 'offset' in self.request.query_params
        ):
            return super().get_paginated_response(data)
        return Response(data)


"""
Так? Можете сформулировать более раскрыто, я не понял как понять ошибку
Логика похожа на версирование, но я попробовал и не получилось
Внутри LimitOffsetPagination была вторая функция и из уроков
Похоже-что она подходит лучше, чем предыдущая, верно?
Или дело было в None, которая была в конце?
"""
