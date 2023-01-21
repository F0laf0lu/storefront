from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer
from django.db.models.aggregates import Count
# Create your views here.

class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer   

    def get_serializer_context(self):
        return {'request':self.request}


class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self,request, id):
        product = get_object_or_404(Product, pk=id)
        try:
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'error': 'Product cannot be deleted because it is associated with an order'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class collectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(product_count=Count('product')).all()
    serializer_class = CollectionSerializer



@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, id):
    collection = get_object_or_404(Collection.objects.annotate(
        product_count=Count('product')), pk=id)
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        try:
            collection.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'error': 'Collection cannot be deleted because it is associated with a product'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
