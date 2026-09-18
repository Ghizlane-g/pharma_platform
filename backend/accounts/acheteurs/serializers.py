from rest_framework import serializers
from accounts.models import User


class AcheteurSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'is_active',
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = User(
            **validated_data,
            role='ACHETEUR'
        )

        user.set_password(password)
        user.save()

        return user