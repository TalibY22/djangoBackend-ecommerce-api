from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from .models import customers,products,cart,cart_item
from rest_framework.authtoken.models import Token
from  .serializers import LoginSerializer,CustomersSerializer,ProductsSerializer,RegisterSerializer,CartSerializer,CartItemSerializer
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
            customer = customers.objects.get(user=user)
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
@api_view(['GET'])
def get_products(request):
    Products = products.objects.all()  # Fetch all products
    serializer = ProductsSerializer(Products, many=True)

    return Response({'products': serializer.data}, status=status.HTTP_201_CREATED)



#Testing phase
@api_view(['POST'])

def create_cart(request):
    print(f"Request User: {request.user}")  # Log the request user
    print(f"Auth Details: {request.headers.get('Authorization')}")
    customer = request.user.customer    
    #get or create check if a cart has been created or note if it has been created return a response 
    Cart, created = cart.objects.get_or_create(customer=customer)
    
    if created:
        message = "A new cart has been created."
    else:
        message = "Existing cart retrieved."

    serializer = CartSerializer(Cart)
    return Response({
        'message': message,
        'cart': serializer.data
    }, status=status.HTTP_200_OK)
    


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_item_to_cart(request):
    customer = request.user.customer
    
    Cart = cart.objects.get(customer=customer)
    
   
    serializer = CartItemSerializer(data=request.data)
    if serializer.is_valid():
        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']
        
        
        try:
            Product = products.objects.get(id=product_id)
        except products.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        
        cart_item, created = cart_item.objects.get_or_create(cart=Cart, product=Product)
        
        if created:
            cart_item.quantity = quantity  
        else:
            cart_item.quantity += quantity  
            
        cart_item.price = Product.price  
        cart_item.save()

       
        #cart.update_total()

        return Response({
            'message': 'Product added to cart',
            'cart_item': CartItemSerializer(cart_item).data
        }, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_cart_with_items(request):
    pass
