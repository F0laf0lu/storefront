from decimal import Decimal
from rest_framework import serializers
from store.models import Collection, Product



class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'product_count']

    product_count = serializers.IntegerField()

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product 
        fields = ['id', 'title','description', 'slug', 'inventory', 'price', 'price_with_tax', 'collection']
        
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    def calculate_tax(self, product):
        return product.price * Decimal(1.1)
