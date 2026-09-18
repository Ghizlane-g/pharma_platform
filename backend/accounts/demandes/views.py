from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from accounts.models import DemandeInscription
from .serializers import DemandeInscriptionSerializer

from django.contrib.auth import get_user_model
User = get_user_model()

@api_view(['POST'])
def creer_demande(request):

    serializer = DemandeInscriptionSerializer(
        data=request.data
    )

    if serializer.is_valid():

        password = serializer.validated_data['password']

        demande = serializer.save(
            password=make_password(password),
            statut='EN_ATTENTE'
        )

        return Response(
            {
                "message": "Votre demande a été envoyée à l'administrateur.",
                "id": demande.id,
                "statut": demande.statut
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def demandes_list(request):

    if request.user.role != 'ADMIN':
        return Response(
            {
                "detail": "Accès réservé à l'administrateur."
            },
            status=status.HTTP_403_FORBIDDEN
        )

    demandes = DemandeInscription.objects.filter(
        statut='EN_ATTENTE'
    ).order_by('-date_creation')

    serializer = DemandeInscriptionSerializer(
        demandes,
        many=True
    )

    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accepter_demande(request, pk):

    if request.user.role != 'ADMIN':
        return Response(
            {"detail": "Accès réservé à l'administrateur."},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        demande = DemandeInscription.objects.get(
            id=pk,
            statut='EN_ATTENTE'
        )
    except DemandeInscription.DoesNotExist:
        return Response(
            {"detail": "Demande introuvable."},
            status=status.HTTP_404_NOT_FOUND
        )

    # Vérifier que le username n'existe pas déjà
    if User.objects.filter(
        username=demande.username
    ).exists():
        return Response(
            {
                "detail": "Ce nom d'utilisateur existe déjà."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # Créer réellement le compte
    user = User(
    username=demande.username,
    email=demande.email,
    password=demande.password,
    role=demande.role,
    first_name=demande.prenom,
    last_name=demande.nom
)

    user.save()

    demande.statut = 'APPROUVEE'
    demande.save()

    return Response(
        {
            "message": "Demande approuvée. Le compte a été créé.",
            "username": user.username,
            "role": user.role
        },
        status=status.HTTP_201_CREATED
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def refuser_demande(request, pk):

    if request.user.role != 'ADMIN':
        return Response(
            {"detail": "Accès réservé à l'administrateur."},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        demande = DemandeInscription.objects.get(
            id=pk,
            statut='EN_ATTENTE'
        )
    except DemandeInscription.DoesNotExist:
        return Response(
            {"detail": "Demande introuvable."},
            status=status.HTTP_404_NOT_FOUND
        )

    demande.statut = 'REFUSEE'
    demande.save()

    return Response(
        {
            "message": "Demande refusée.",
            "id": demande.id,
            "statut": demande.statut
        },
        status=status.HTTP_200_OK
    )