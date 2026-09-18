from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from accounts.models import Medicament
from accounts.permissions import IsAdmin

from .serializers import MedicamentSerializer


class MedicamentViewSet(viewsets.ModelViewSet):
    queryset = Medicament.objects.all()
    serializer_class = MedicamentSerializer
    permission_classes = [IsAdmin]

    @action(detail=True, methods=['patch'])
    def desactiver(self, request, pk=None):

        medicament = self.get_object()

        medicament.statut = "NON_DISPONIBLE"
        medicament.save()

        return Response(
            {
                "message": "Médicament désactivé avec succès.",
                "id": medicament.id,
                "nom": medicament.nom,
                "statut": medicament.statut
            },
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['patch'])
    def activer(self, request, pk=None):

        medicament = self.get_object()

        medicament.statut = "DISPONIBLE"
        medicament.save()

        return Response(
            {
                "message": "Médicament activé avec succès.",
                "id": medicament.id,
                "nom": medicament.nom,
                "statut": medicament.statut
            },
            status=status.HTTP_200_OK
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_medicament(request):

    if request.user.role != "ADMIN":
        return Response(
            {"detail": "Accès réservé à l'administrateur."},
            status=status.HTTP_403_FORBIDDEN
        )

    nom = request.data.get("nom")
    classe = request.data.get("classe")
    prix = request.data.get("prix")
    statut = request.data.get("statut", "DISPONIBLE")

    if not nom or not classe or not prix:
        return Response(
            {"detail": "Nom, classe et prix sont obligatoires."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if statut not in ["DISPONIBLE", "NON_DISPONIBLE"]:
        statut = "DISPONIBLE"

    medicament = Medicament.objects.create(
        nom=nom,
        classe=classe,
        prix=prix,
        statut=statut
    )

    return Response(
        {
            "message": "Médicament créé avec succès.",
            "id": medicament.id,
            "nom": medicament.nom,
            "classe": medicament.classe,
            "prix": medicament.prix,
            "statut": medicament.statut,
        },
        status=status.HTTP_201_CREATED
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def medicaments_disponibles(request):

    medicaments = Medicament.objects.filter(
        statut="DISPONIBLE"
    )

    data = []

    for medicament in medicaments:
        data.append({
            "id": medicament.id,
            "nom": medicament.nom,
            "classe": medicament.classe,
            "prix": str(medicament.prix),
            "statut": medicament.statut,
        })

    return Response(data, status=status.HTTP_200_OK)