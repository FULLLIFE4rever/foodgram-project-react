from rest_framework.pagination import LimitOffsetPagination


class LimitMaxPageNumberPagination(LimitOffsetPagination):
    """Класс пагинации страниц."""

    max_page_size = 20
