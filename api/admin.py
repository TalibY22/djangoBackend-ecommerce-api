from django.contrib import admin
from .models import products,customer_payments,customers,category,wishlist

# Register your models here.

admin.site.register(products)
admin.site.register(customer_payments)
admin.site.register(customers)
admin.site.register(category)
admin.site.register(wishlist)
