from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from .models import customers
from rest_framework.authtoken.models import Token
from  .serializers import LoginSerializer,CustomersSerializer,ProductsSerializer,RegisterSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


@api_view(['POST'])
def login_api(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            customer = customer.objects.get(user=user)
            customer_Serializer = CustomersSerializer(customer)
            return Response({'token': token.key,'customer_details':customer_Serializer.data})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def register_api(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        first_name = serializer.validated_data['first_name']
        last_name = serializer.validated_data['last_name']
        email = serializer.validated_data['email']
        phone_number = serializer.validated_data['phone_number']
        address = serializer.validated_data['address']
        dob = serializer.validated_data['dob']

        customer = customers(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            address=address,
            dob=dob
        )
        
        # Save the customer instance to the database
        customer.save()

        return Response({'message': 'Customer registered successfully'}, status=status.HTTP_201_CREATED)

    else:
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
