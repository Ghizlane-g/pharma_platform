from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from rest_framework import status
from .models import User,Commande,Medicament
from .serializers import UserSerializer
from .permissions import IsAdmin
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import StockAcheteur, Medicament
from .serializers import StockAcheteurSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def statistics(request):

    if request.user.role != 'ADMIN':
        return Response(
            {'detail': 'Accès réservé à l’administrateur.'},
            status=403
        )

    total_comptes = User.objects.count()
    total_acheteurs = User.objects.filter(role='ACHETEUR').count()
    total_clients = User.objects.filter(role='CLIENT').count()
    total_commandes = Commande.objects.count()
    total_medicaments = Medicament.objects.count()
    return Response({
        'total_comptes': total_comptes,
        'acheteurs': total_acheteurs,
        'clients': total_clients,
        'commandes': total_commandes,
        'medicaments': total_medicaments,
    })
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def accounts_list(request):

    if request.user.role != 'ADMIN':
        return Response(
            {'detail': 'Accès réservé à l’administrateur.'},
            status=403
        )

    users = User.objects.all()

    data = []

    for user in users:
        data.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
        })

    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def clients_list(request):

    if request.user.role != 'ADMIN':
        return Response(
            {'detail': 'Accès réservé à l’administrateur.'},
            status=403
        )

    clients = User.objects.filter(role='CLIENT')

    data2 = []

    for client in clients:
        data2.append({
            'id': client.id,
            'username': client.username,
            'email': client.email,
            'first_name': client.first_name,
            'last_name': client.last_name,
        })

    return Response(data2)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def commandes_list(request):

    if request.user.role != 'ADMIN':
        return Response(
            {'detail': 'Accès réservé à l’administrateur.'},
            status=403
        )

    commandes = Commande.objects.select_related('client').all()

    dataCommande = []

    for commande in commandes:
        dataCommande.append({
            'id': commande.id,
            'client_id': commande.client.id,
            'client_username': commande.client.username,
            'date_creation': commande.date_creation,
            'statut': commande.statut,
            'total': str(commande.total),
        })

    return Response(dataCommande)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def medicaments_list(request):

    if request.user.role != 'ADMIN':
        return Response(
            {'detail': 'Accès réservé à l’administrateur.'},
            status=403
        )

    medicaments = Medicament.objects.all()

    dataMedicaments = []

    for medicament in medicaments:
        dataMedicaments.append({
            'id': medicament.id,
            'nom': medicament.nom,
            'classe': medicament.classe,
            'prix': str(medicament.prix),
            'statut': medicament.statut,
            'date_creation': medicament.date_creation,
        })

    return Response(dataMedicaments)


#Client views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def client_medicaments_list(request):

    if request.user.role != 'CLIENT':
        return Response(
            {'detail': 'Accès réservé au client.'},
            status=403
        )

    medicaments = Medicament.objects.filter(
        statut='DISPONIBLE'
    )

    dataMedicaments = []

    for medicament in medicaments:
        dataMedicaments.append({
            'id': medicament.id,
            'nom': medicament.nom,
            'classe': medicament.classe,
            'prix': str(medicament.prix),
            'statut': medicament.statut,
            'date_creation': medicament.date_creation,
        })

    return Response(dataMedicaments)

#acheteur views

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mon_stock(request):

    if request.user.role != "ACHETEUR":
        return Response(
            {
                "detail": "Accès réservé à l'acheteur."
            },
            status=status.HTTP_403_FORBIDDEN
        )

    stocks = StockAcheteur.objects.filter(
        acheteur=request.user
    ).select_related('medicament')

    serializer = StockAcheteurSerializer(
        stocks,
        many=True
    )

    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ajouter_stock(request):

    if request.user.role != "ACHETEUR":
        return Response(
            {
                "detail": "Accès réservé à l'acheteur."
            },
            status=status.HTTP_403_FORBIDDEN
        )

    medicament_id = request.data.get("medicament")
    quantite = request.data.get("quantite")

    if not medicament_id or not quantite:
        return Response(
            {
                "detail": "Le médicament et la quantité sont obligatoires."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        medicament_id = int(medicament_id)
        quantite = int(quantite)
    except (TypeError, ValueError):
        return Response(
            {
                "detail": "Le médicament ou la quantité est invalide."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    if quantite <= 0:
        return Response(
            {
                "detail": "La quantité doit être supérieure à 0."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        medicament = Medicament.objects.get(
            id=medicament_id
        )
    except Medicament.DoesNotExist:
        return Response(
            {
                "detail": "Médicament introuvable."
            },
            status=status.HTTP_404_NOT_FOUND
        )

    stock, created = StockAcheteur.objects.get_or_create(
        acheteur=request.user,
        medicament=medicament,
        defaults={
            "quantite": quantite
        }
    )

    if not created:
        stock.quantite += quantite
        stock.save()

    serializer = StockAcheteurSerializer(stock)

    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED
    )

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def modifier_stock(request, pk):

    if request.user.role != "ACHETEUR":
        return Response(
            {"detail": "Accès réservé à l'acheteur."},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        stock = StockAcheteur.objects.get(
            id=pk,
            acheteur=request.user
        )
    except StockAcheteur.DoesNotExist:
        return Response(
            {"detail": "Stock introuvable."},
            status=status.HTTP_404_NOT_FOUND
        )

    quantite = request.data.get("quantite")

    try:
        quantite = int(quantite)
    except (TypeError, ValueError):
        return Response(
            {"detail": "La quantité doit être un nombre."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if quantite < 0:
        return Response(
            {"detail": "La quantité ne peut pas être négative."},
            status=status.HTTP_400_BAD_REQUEST
        )

    stock.quantite = quantite
    stock.save()

    serializer = StockAcheteurSerializer(stock)

    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def supprimer_stock(request, pk):

    if request.user.role != "ACHETEUR":
        return Response(
            {"detail": "Accès réservé à l'acheteur."},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        stock = StockAcheteur.objects.get(
            id=pk,
            acheteur=request.user
        )
    except StockAcheteur.DoesNotExist:
        return Response(
            {"detail": "Stock introuvable."},
            status=status.HTTP_404_NOT_FOUND
        )

    stock.delete()

    return Response(
        {
            "message": "Médicament retiré du stock."
        },
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def liste_medicaments_acheteur(request):

    if request.user.role != "ACHETEUR":
        return Response(
            {"detail": "Accès réservé à l'acheteur."},
            status=status.HTTP_403_FORBIDDEN
        )

    medicaments = Medicament.objects.all().order_by('nom')

    data = []

    for medicament in medicaments:
        data.append({
            "id": medicament.id,
            "nom": medicament.nom,
            "classe": medicament.classe,
            "prix": str(medicament.prix),
            "statut": medicament.statut,
        })

    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stock_acheteurs(request):

    if request.user.role != "ADMIN":
        return Response(
            {"detail": "Accès réservé à l'administrateur."},
            status=status.HTTP_403_FORBIDDEN
        )

    stocks = StockAcheteur.objects.select_related(
        'acheteur',
        'medicament'
    ).order_by(
        'medicament__nom',
        'acheteur__username'
    )

    data = []

    for stock in stocks:

        data.append({
            "id": stock.id,
            "medicament_id": stock.medicament.id,
            "medicament_nom": stock.medicament.nom,
            "acheteur_id": stock.acheteur.id,
            "acheteur_username": stock.acheteur.username,
            "quantite": stock.quantite,
            "date_ajout": stock.date_ajout,
        })

    return Response(data)