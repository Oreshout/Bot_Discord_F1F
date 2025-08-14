from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, CoinTransaction, Product

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Inclut les infos User dans le profil

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'coins']

class CoinTransactionSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = CoinTransaction
        fields = ['id', 'user_profile', 'amount', 'description', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
