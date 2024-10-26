from .models import (customers, category, products, wishlist, cart, 
                    cart_item, orders, order_items, payments, customer_payments)
from rest_framework import serializers
from django.contrib.auth.models import Group, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = customers
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category_type = CategorySerializer(read_only=True)
    
    class Meta:
        model = products
        fields = '__all__'

class WishlistSerializer(serializers.ModelSerializer):
    product_id = ProductSerializer(read_only=True)
    
    class Meta:
        model = wishlist
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    product_id = ProductSerializer(read_only=True)
    
    class Meta:
        model = cart_item
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True, source='cart_item_set')
    
    class Meta:
        model = cart
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    product_id = ProductSerializer(read_only=True)
    
    class Meta:
        model = order_items
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True, source='order_items_set')
    
    class Meta:
        model = orders
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = payments
        fields = '__all__'

class CustomerPaymentSerializer(serializers.ModelSerializer):
    payment_id = PaymentSerializer(read_only=True)
    
    class Meta:
        model = customer_payments
        fields = '__all__'