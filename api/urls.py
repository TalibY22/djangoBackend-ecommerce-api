from django.contrib import admin
from django.urls import path
from .import views


urlpatterns = [
   
     path('api/login',views.login_api),
     #Path for applying for leave try it out in the post leave form
    
    
]