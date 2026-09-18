from rest_framework import serializers
from accounts.models import Commande, LigneCommande, Medicament


class LigneCommandeSerializer(serializers.ModelSerializer):
    medicament_nom = serializers.CharField(
        source='medicament.nom',
        read_only=True
    )

    class Meta:
        model = LigneCommande
        fields = [
            'medicament',
            'medicament_nom',
            'quantite',
            'prix_unitaire',
        ]


class CommandeSerializer(serializers.ModelSerializer):
    client_username = serializers.CharField(
        source='client.username',
        read_only=True
    )

    lignes = LigneCommandeSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Commande
        fields = [
            'id',
            'client',
            'client_username',
            'lignes',
            'date_creation',
            'statut',
            'total',
        ]