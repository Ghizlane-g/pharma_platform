from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from accounts.models import User
from .serializers import AcheteurSerializer
from accounts.permissions import IsAdmin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

class AcheteurViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(role='ACHETEUR')
    serializer_class = AcheteurSerializer
    permission_classes = [IsAdmin]

    @action(detail=True, methods=['patch'])
    def desactiver(self, request, pk=None):
        acheteur = self.get_object()

        acheteur.is_active = False
        acheteur.save()

        return Response(
            {
                "message": "Acheteur désactivé avec succès."
            },
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['patch'])
    def activer(self, request, pk=None):
        acheteur = self.get_object()

        acheteur.is_active = True
        acheteur.save()

        return Response(
            {
                "message": "Acheteur activé avec succès."
            },
            status=status.HTTP_200_OK
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_acheteur(request):

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

    acheteur = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        role="ACHETEUR"
    )

    return Response(
        {
            "message": "Acheteur créé avec succès.",
            "id": acheteur.id,
            "username": acheteur.username,
            "email": acheteur.email,
            "role": acheteur.role
        },
        status=status.HTTP_201_CREATED
    )