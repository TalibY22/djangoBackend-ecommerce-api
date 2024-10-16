from django.contrib import admin
from django.urls import path
from .import views


urlpatterns = [
   
     path('api/login',views.login_api),
     path('api/register',views.register_api),
     path('api/products',views.get_products),
     path('api/create_cart',views.create_cart),


     #Path for applying for leave try it out in the post leave form
    
    
]