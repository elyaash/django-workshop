from decimal import Decimal
from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'title2','description', 'slug', 'inventory',
                  'unit_price', 'price_with_tax', 'collection']

    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')
    
    title2 = serializers.SerializerMethodField(
        method_name='title2_field')

    def title2_field(self,product:Product):
        return product.title.upper()
    
    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
