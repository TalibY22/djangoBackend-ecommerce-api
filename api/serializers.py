from .models import customers,products
from rest_framework import serializers
from django.contrib.auth.models import Group, User


class CustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = customers
        fields = ['first_name', 'last_name', 'email', 'phone_number','address','dob']


class ProductsSerializer(serializers.ModelSerializer):

    class Meta:
        model = products
        fields='__all__'

#should return customer_details
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
     first_name  = serializers.CharField()
     last_name  = serializers.CharField()
     email = serializers.EmailField()
     phone_number = serializers.IntegerField()
     address = serializers.CharField()
     dob = serializers.DateField()

     
class CartSerializer(serializers.Serializer):
     customer_id = serializers.IntegerField()
     total = serializers.IntegerField()

class CartItemSerializer(serializers.Serializer):
      cart_id = serializers.IntegerField()
      product_id = serializers.IntegerField()
      quantity = serializers.IntegerField()
      
