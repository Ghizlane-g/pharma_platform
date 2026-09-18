from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from accounts.models import Commande , Medicament, LigneCommande
from .serializers import CommandeSerializer
from accounts.permissions import IsAdmin
class CommandeViewSet(viewsets.ModelViewSet):

    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer
    permission_classes = [IsAdmin]

    @action(detail=True, methods=['patch'])
    def changer_statut(self, request, pk=None):

        commande = self.get_object()

        nouveau_statut = request.data.get("statut")

        statuts_valides = [
            "EN_ATTENTE",
            "EN_COURS",
            "LIVREE",
            "ANNULEE"
        ]

        if nouveau_statut not in statuts_valides:
            return Response(
                {
                    "detail": "Statut invalide."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        commande.statut = nouveau_statut
        commande.save()

        return Response(
            {
                "message": "Statut modifié avec succès.",
                "id": commande.id,
                "statut": commande.statut
            },
            status=status.HTTP_200_OK
        )

# client

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def creer_commande(request):

    if request.user.role != "CLIENT":
        return Response(
            {"detail": "Accès réservé au client."},
            status=status.HTTP_403_FORBIDDEN
        )

    medicaments = request.data.get("medicaments")

    if not medicaments:
        return Response(
            {"detail": "Aucun médicament sélectionné."},
            status=status.HTTP_400_BAD_REQUEST
        )

    commande = Commande.objects.create(
        client=request.user,
        statut="EN_ATTENTE",
        total=0
    )

    total = 0

    for item in medicaments:

        medicament_id = item.get("medicament_id")
        quantite = item.get("quantite", 1)

        try:
            quantite = int(quantite)
        except (TypeError, ValueError):
            commande.delete()
            return Response(
                {"detail": "Quantité invalide."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if quantite <= 0:
            commande.delete()
            return Response(
                {"detail": "La quantité doit être supérieure à 0."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            medicament = Medicament.objects.get(
                id=medicament_id,
                statut="DISPONIBLE"
            )
        except Medicament.DoesNotExist:
            commande.delete()
            return Response(
                {
                    "detail": f"Le médicament {medicament_id} "
                               "n'est pas disponible."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        prix = medicament.prix

        LigneCommande.objects.create(
            commande=commande,
            medicament=medicament,
            quantite=quantite,
            prix_unitaire=prix
        )

        total += prix * quantite

    commande.total = total
    commande.save()

    return Response(
        {
            "message": "Commande créée avec succès.",
            "id": commande.id,
            "statut": commande.statut,
            "total": str(commande.total)
        },
        status=status.HTTP_201_CREATED
    )



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mes_commandes(request):

    commandes = Commande.objects.filter(
        client=request.user
    ).prefetch_related(
        'lignes__medicament'
    ).order_by('-date_creation')

    serializer = CommandeSerializer(
        commandes,
        many=True
    )

    return Response(serializer.data)