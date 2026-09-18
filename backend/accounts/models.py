from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
# Create your models here.


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        ACHETEUR = "ACHETEUR", "Acheteur"
        CLIENT = "CLIENT", "Client"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.ADMIN
    )

class Commande(models.Model):

    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('EN_COURS', 'En cours'),
        ('LIVREE', 'Livrée'),
        ('ANNULEE', 'Annulée'),
    ]

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='commandes'
    )

    date_creation = models.DateTimeField(auto_now_add=True)

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='EN_ATTENTE'
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"Commande {self.id}"
        
class Medicament(models.Model):

    STATUT_CHOICES = [
        ('DISPONIBLE', 'Disponible'),
        ('NON_DISPONIBLE', 'Non disponible'),
    ]

    CLASSE_CHOICES = [
        ('ANTALGIQUES', 'Antalgiques'),
        ('ANTIBIOTIQUES', 'Antibiotiques'),
        ('ANTI_INFLAMMATOIRES', 'Anti-inflammatoires'),
        ('VITAMINES', 'Vitamines'),
        ('DIGESTIFS', 'Digestifs'),
        ('CARDIOLOGIE', 'Cardiologie'),
        ('AUTRES', 'Autres'),
    ]

    nom = models.CharField(max_length=100)

    prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    classe = models.CharField(
        max_length=50,
        choices=CLASSE_CHOICES,
        default='AUTRES'
    )

    statut = models.CharField(
        max_length=15,
        choices=STATUT_CHOICES,
        default='DISPONIBLE'
    )

    date_creation = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = 'accounts_medicament'

    def __str__(self):
        return self.nom


class StockAcheteur(models.Model):

    acheteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='stocks'
    )

    medicament = models.ForeignKey(
        Medicament,
        on_delete=models.CASCADE,
        related_name='stocks_acheteurs'
    )

    quantite = models.PositiveIntegerField(
        default=0
    )

    date_ajout = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('acheteur', 'medicament')

    def __str__(self):
        return f"{self.acheteur.username} - {self.medicament.nom} - {self.quantite}"


class LigneCommande(models.Model):

    commande = models.ForeignKey(
        'Commande',
        on_delete=models.CASCADE,
        related_name='lignes'
    )

    medicament = models.ForeignKey(
        'Medicament',
        on_delete=models.CASCADE,
        related_name='lignes_commandes'
    )

    quantite = models.PositiveIntegerField(default=1)

    prix_unitaire = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.medicament.nom} x {self.quantite}"
    
class DemandeInscription(models.Model):

    ROLE_CHOICES = [
        ('CLIENT', 'Client'),
        ('ACHETEUR', 'Acheteur'),
    ]

    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('APPROUVEE', 'Approuvée'),
        ('REFUSEE', 'Refusée'),
    ]

    nom = models.CharField(max_length=100)

    prenom = models.CharField(max_length=100)

    email = models.EmailField()

    username = models.CharField(
        max_length=150,
        unique=True
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    # Le mot de passe sera stocké sous forme hashée
    password = models.CharField(max_length=128)

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='EN_ATTENTE'
    )

    date_creation = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.username} - {self.role}"