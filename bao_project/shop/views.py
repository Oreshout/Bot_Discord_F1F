from rest_framework import viewsets
from .models import Product, UserProfile, CoinTransaction
from .serializers import ProductSerializer, UserProfileSerializer, CoinTransactionSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class CoinTransactionViewSet(viewsets.ModelViewSet):
    queryset = CoinTransaction.objects.all()
    serializer_class = CoinTransactionSerializer
