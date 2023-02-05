from store.pagination import DefaultPagination
from django.db.models.aggregates import Count
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import ProductFilter
from .models import Product, Collection, OrderItem, Review
from rest_framework.viewsets import ModelViewSet
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer

# Create your views here.



class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer   
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    filterset_fields =  ['collection_id', 'price', 'inventory']
    search_fields = ['title', 'description']
    ordering_fields = ['price','last_update']



    def get_serializer_context(self):
        return {'request':self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id = kwargs['pk']):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super().destroy(request, *args, **kwargs)    


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(product_count=Count('product')).all()
    serializer_class = CollectionSerializer
    
    def destroy(self, request, *args, **kwargs):
        if Collection.objects.filter(collection_id = kwargs['pk']):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    # def get_serializer_context(self):
    #     return {'product_id': self.kwargs['product_pk']}
