from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CustomerViewSet,CartViewSet,ProductViewSet,CategoryViewSet,WishlistViewSet,OrderViewSet,PaymentViewSet,test_history

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'wishlist', WishlistViewSet, basename='wishlist')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'payments', PaymentViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('test-history/', test_history, name='test-history'),
    
]