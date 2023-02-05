import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    class meta:
        model= Product
        fields = {
            'collection_id':['exact']
        }