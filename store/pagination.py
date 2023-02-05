from rest_framework.pagination import PageNumberPagination

class DefaultPagination(PageNumberPagination):
    pagesize = 10