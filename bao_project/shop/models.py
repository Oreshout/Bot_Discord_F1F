from django.db import models
from django.contrib.auth.models import User  # modèle utilisateur Django de base

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    # Liaison 1 à 1 avec User, si User supprimé, le profil aussi

    coins = models.IntegerField(default=0)  
    # Solde de coins, valeur entière par défaut 0

    def __str__(self):
        return f"{self.user.username} - {self.coins} coins"

class CoinTransaction(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='transactions')
    # Plusieurs transactions pour un profil utilisateur

    amount = models.IntegerField()
    # Nombre de coins gagnés (positif) ou dépensés (négatif)

    description = models.CharField(max_length=255, blank=True)
    # Optionnel, détail de la transaction (ex : "Achat T-shirt")

    created_at = models.DateTimeField(auto_now_add=True)
    # Date de création automatique

    def __str__(self):
        type_trans = "Gain" if self.amount > 0 else "Dépense"
        return f"{type_trans} {abs(self.amount)} coins pour {self.user_profile.user.username}"

class Product(models.Model):
    VIRTUAL = 'virtual'
    REAL = 'real'
    PRODUCT_TYPE_CHOICES = [
        (VIRTUAL, 'Virtuel'),
        (REAL, 'Physique'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price_coins = models.IntegerField()
    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPE_CHOICES, default=VIRTUAL)
    stock = models.IntegerField(default=0)
    # stock = 0 signifie "illimité" ou en rupture ? À définir

    def __str__(self):
        return f"{self.name} ({self.price_coins} coins)"
