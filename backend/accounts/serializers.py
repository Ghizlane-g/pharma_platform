from .models import User, StockAcheteur
from rest_framework import serializers 


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'role',
            'is_active',
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.pop('password', None)

        user = User(**validated_data)

        if password:
            user.set_password(password)

        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance
        


from rest_framework import serializers
from .models import StockAcheteur


class StockAcheteurSerializer(serializers.ModelSerializer):

    medicament_nom = serializers.CharField(
        source="medicament.nom",
        read_only=True
    )

    acheteur_username = serializers.CharField(
        source="acheteur.username",
        read_only=True
    )

    class Meta:
        model = StockAcheteur
        fields = [
            "id",
            "acheteur",
            "acheteur_username",
            "medicament",
            "medicament_nom",
            "quantite",
            "date_ajout",
        ]

        read_only_fields = [
            "id",
            "acheteur",
            "date_ajout",
        ]