from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, UserProfileViewSet, CoinTransactionViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'userprofiles', UserProfileViewSet)
router.register(r'transactions', CoinTransactionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
