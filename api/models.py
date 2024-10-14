from django.db import models
from typing import Any, Iterable
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from datetime import timedelta

# Create your models here.

class customers(models.Model):
     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
     first_name  = models.CharField(max_length=20)
     last_name = models.CharField(max_length=20)
     email = models.EmailField()
     phone_number = models.IntegerField()
     address = models.CharField()
     dob = models.DateField()

     #Create a user for the customers 
     def save(self, *args, **kwargs):
        if not self.user:
           
            username = self.First_Name.lower()
            password = "123456789"  

            
            self.user = User.objects.create_user(username=username, password=password)
        
        
        super().save(*args, **kwargs)


class category(models.Model):
    category_type = models.CharField(max_length=20)



class products(models.Model):

    name = models.CharField(max_length=200)
    price = models.IntegerField()
    descrption = models.CharField(max_length=200)
    summary = models.CharField(max_length=200)
    SKU = models.IntegerField()
    
    category_type = models.ForeignKey(category, on_delete=models.CASCADE)


class wishlist(models.Model):
      customer_id = models.ForeignKey(customers, on_delete=models.CASCADE)
      product_id = models.ForeignKey(products, on_delete=models.CASCADE)


class cart(models.Model):
      customer_id = models.ForeignKey(customers, on_delete=models.CASCADE)
      total = models.IntegerField()


class cart_item(models.Model):
       cart_id = models.ForeignKey(cart, on_delete=models.CASCADE)
       product_id = models.ForeignKey(products, on_delete=models.CASCADE)
       quantity = models.IntegerField()

class orders(models.Model):
      customers = models.ForeignKey(customers, on_delete=models.CASCADE)
      type = models.CharField(max_length=20)

      total = models.IntegerField()


class order_items(models.Model):
      order_id = models.ForeignKey(orders, on_delete=models.CASCADE)
      product_id = models.ForeignKey(products,on_delete=models.CASCADE)



class payments(models.Model):
      order_id = models.ForeignKey(orders, on_delete=models.CASCADE)
      payment_method = models.CharField(max_length=256)
      amount_paid = models.IntegerField()
      date_of_payment = models.IntegerField()

class customer_payments(models.Model):
      customer_id = models.ForeignKey(customers, on_delete=models.CASCADE)
      payment_id = models.ForeignKey(payments, on_delete=models.CASCADE)







    
