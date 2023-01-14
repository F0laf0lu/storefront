from django.contrib import admin
from django.db.models.aggregates import Count
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode
from . models import Collection, Product, Customer, Order

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'inventory_status', 'collection']
    list_per_page = 10
    list_editable = ['price']
    list_select_related = ['collection']

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'customer_orders']
    list_per_page = 10
    list_editable = ['membership']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='customer_orders')
    def customer_orders(self, customer):
        return customer.customer_orders
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(customer_orders = Count('order'))

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_count']

    @admin.display(ordering='product_count')
    def product_count(self, collection):
        url = (
            reverse("admin:store_product_changelist") 
            + '?' 
            + urlencode({
            'collection__id' : str(collection.id)
            }))
        return format_html('<a href="{}">{}</a>', url, collection.product_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            product_count=Count('product')
            )



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'payment_status', 'customer']
