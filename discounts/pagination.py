from rest_framework import pagination


class PromocodePagination(pagination.PageNumberPagination):
    page_size = 20

class StorePagination(pagination.PageNumberPagination):
    page_size = 5