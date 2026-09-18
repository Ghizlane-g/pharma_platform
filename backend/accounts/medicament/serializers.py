from rest_framework import serializers
from accounts.models import Medicament


class MedicamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicament
        fields = [
            'id',
            'nom',
            'classe',
            'prix',
            'statut',
            'date_creation'
        ]