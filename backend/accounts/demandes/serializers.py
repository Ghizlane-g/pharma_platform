from rest_framework import serializers

from accounts.models import DemandeInscription


class DemandeInscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = DemandeInscription

        fields = [
            'id',
            'nom',
            'prenom',
            'email',
            'username',
            'password',
            'role',
            'statut',
            'date_creation',
        ]

        read_only_fields = [
            'id',
            'statut',
            'date_creation',
        ]

        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate_username(self, value):

        if DemandeInscription.objects.filter(
            username=value,
            statut='EN_ATTENTE'
        ).exists():

            raise serializers.ValidationError(
                "Une demande avec ce nom d'utilisateur est déjà en attente."
            )

        return value