from django.contrib import admin
from .models import UserProfile, CoinTransaction, Product

admin.site.register(UserProfile)
admin.site.register(CoinTransaction)
admin.site.register(Product)
