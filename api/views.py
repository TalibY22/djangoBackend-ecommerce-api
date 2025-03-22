from rest_framework import viewsets, status
from rest_framework.decorators import action,api_view
from logging import Logger
from rest_framework.response import Response
from .serializers import UserSerializer,CartItemSerializer,CustomerSerializer,CategorySerializer,ProductSerializer,WishlistSerializer,CartSerializer,OrderSerializer,TestSerializer,PaymentSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import (customers, category, products, wishlist, cart, 
                    cart_item, orders, order_items, payments, customer_payments,Test)
from django.shortcuts import get_object_or_404

from django.core.cache import cache 

@api_view(['GET', 'POST'])
def test_history(request):
    cache_key = "test_history_data"  # Unique key for caching test data

    if request.method == 'GET':
        cached_data = cache.get(cache_key)  # Check if data is in Redis
        if cached_data:
            return Response({"status": "✅ Cached", "data": cached_data})

        test_records = Test.objects.all()
        serializer = TestSerializer(test_records, many=True)

        cache.set(cache_key, serializer.data, timeout=60 * 5)  # Cache for 5 minutes
        return Response({"status": "❌ Not Cached (Fetching)", "data": serializer.data})

    elif request.method == 'POST':
        serializer = TestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            # Clear cache so next GET request fetches fresh data
            cache.delete(cache_key)  

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = customers.objects.all()
    serializer_class = CustomerSerializer
    
    def get_permissions(self):
        if self.action in ['create']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return customers.objects.all()
        return customers.objects.filter(user=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]



class ProductViewSet(viewsets.ModelViewSet):
    queryset = products.objects.all()
    serializer_class = ProductSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]
    
    @action(detail=False, methods=['GET'])
    def by_category(self, request):
        category_id = request.query_params.get('category_id')
        products_list = products.objects.filter(category_type_id=category_id)

        cache_key = f"products_category_{category_id}"  
        cached_data = cache.get(cache_key)

        if cached_data:
            Logger.info("returning cached data ")
            return Response(cached_data)


        serializer = self.get_serializer(products_list, many=True)
        print("cache missing ")
        cache.set(cache_key, serializer.data, timeout=60 * 5)
        return Response(serializer.data)

class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return wishlist.objects.filter(customer_id__user=self.request.user)

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return cart.objects.filter(customer_id__user=self.request.user)
    
    def create(self, request):
        """
        Create a new cart if user doesn't have one
        """
        # Check if user already has a cart
        customer_instance = get_object_or_404(customers, user=request.user)
        existing_cart = cart.objects.filter(customer_id=customer_instance).first()
        
        if existing_cart:
            return Response(
                {"detail": "Cart already exists for this user"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create new cart
        cart_instance = cart.objects.create(
            customer_id=customer_instance,
            total=0.00
        )
        serializer = self.get_serializer(cart_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['POST'])
    def add_item(self, request, pk=None):
        """
        Add item to cart with quantity
        """
        cart_instance = self.get_object()
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        
        # Validate product
        product_instance = get_object_or_404(products, id=product_id)
        
        # Check if item already exists in cart
        existing_item = cart_item.objects.filter(
            cart_id=cart_instance,
            product_id=product_instance
        ).first()
        
        if existing_item:
            # Update quantity if item exists
            existing_item.quantity += quantity
            existing_item.save()
        else:
            # Create new cart item
            cart_item.objects.create(
                cart_id=cart_instance,
                product_id=product_instance,
                price=product_instance.price,
                quantity=quantity
            )
        
        # Update cart total
        self._update_cart_total(cart_instance)
        
        return Response({'status': 'Item added to cart'})
    
    @action(detail=True, methods=['POST'])
    def remove_item(self, request, pk=None):
        """
        Remove item from cart
        """
        cart_instance = self.get_object()
        product_id = request.data.get('product_id')
        
        cart_item.objects.filter(
            cart_id=cart_instance,
            product_id=product_id
        ).delete()
        
        # Update cart total
        self._update_cart_total(cart_instance)
        
        return Response({'status': 'Item removed from cart'})
    
    def _update_cart_total(self, cart_instance):
        """
        Update cart total based on items
        """
        cart_items = cart_item.objects.filter(cart_id=cart_instance)
        total = sum(item.price * item.quantity for item in cart_items)
        cart_instance.total = total
        cart_instance.save()

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return orders.objects.all()
        return orders.objects.filter(customers__user=self.request.user)
    
    @action(detail=False, methods=['POST'])
    def create_from_cart(self, request):
        customer = get_object_or_404(customers, user=request.user)
        cart_instance = get_object_or_404(cart, customer_id=customer)
        
        # Create order
        order = orders.objects.create(
            customers=customer,
            type='online',
            total=cart_instance.total
        )
        
        # Create order items from cart items
        cart_items = cart_item.objects.filter(cart_id=cart_instance)
        for item in cart_items:
            order_items.objects.create(
                order_id=order,
                product_id=item.product_id,
            )
        
        # Clear cart
        cart_items.delete()
        cart_instance.total = 0
        cart_instance.save()
        
        return Response({'status': 'Order created successfully'})

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = payments.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return payments.objects.all()
        return payments.objects.filter(order_id__customers__user=self.request.user)
