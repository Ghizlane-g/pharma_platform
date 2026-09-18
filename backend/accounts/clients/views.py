from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from accounts.models import User
from .serializers import ClientSerializer
from accounts.permissions import IsAdmin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

class ClientViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(role='CLIENT')
    serializer_class = ClientSerializer
    permission_classes = [IsAdmin]

    @action(detail=True, methods=['patch'])
    def desactiver(self, request, pk=None):
        client = self.get_object()

        client.is_active = False
        client.save()

        return Response(
            {
                "message": "Client désactivé avec succès."
            },
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['patch'])
    def activer(self, request, pk=None):
        client = self.get_object()

        client.is_active = True
        client.save()

        return Response(
            {
                "message": "Client activé avec succès."
            },
            status=status.HTTP_200_OK
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_client(request):

    if request.user.role != "ADMIN":
        return Response(
            {"detail": "Accès réservé à l'administrateur."},
            status=status.HTTP_403_FORBIDDEN
        )

    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if not username or not email or not password:
        return Response(
            {"detail": "Tous les champs sont obligatoires."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"detail": "Ce username existe déjà."},
            status=status.HTTP_400_BAD_REQUEST
        )

    client = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        role="CLIENT"
    )

    return Response(
        {
            "message": "Client créé avec succès.",
            "id": client.id,
            "username": client.username,
            "email": client.email,
            "role": client.role
        },
        status=status.HTTP_201_CREATED
    )