from django.urls import path
from .views import (login_page, dashboard,acheteurs,comptes,clients,commandes,medicaments,logout_view,Ajouter_Acheteur,modifier_acheteur,desactiver_acheteur,activer_acheteur,Ajouter_Client,modifier_client,activer_client,desactiver_client,ajouter_medicament,modifier_medicament,desactiver_medicament,activer_medicament,modifier_statut_commande,client_dashboard,client_commandes,register_view,demandes_inscription,accepter_demande_frontend,refuser_demande_frontend,ajouter_panier,panier,
    retirer_panier,
    modifier_quantite_panier,
    vider_panier,
    valider_commande,acheteur_stock ,ajouter_stock_frontend,supprimer_stock_frontend,modifier_stock_frontend,stock_acheteurs,)
urlpatterns = [
    path('', login_page, name='home'),
    path('login/', login_page, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('comptes/', comptes, name='comptes'),
    path('acheteurs/', acheteurs, name='acheteurs'),
    path('clients/', clients, name='clients'),
    path('commandes/', commandes, name='commandes'),
    path('medicaments/', medicaments, name='medicaments'),
    path('logout/', logout_view, name='logout'),
    path('acheteurs/ajouter/',Ajouter_Acheteur,name='Ajouter_Acheteur'),
    path('acheteurs/modifier/<int:id>/', modifier_acheteur, name='modifier_acheteur'),
    path('acheteurs/desactiver/<int:id>/',desactiver_acheteur,name='desactiver_acheteur'),
    path(
    'acheteurs/activer/<int:id>/',
    activer_acheteur,
    name='activer_acheteur'
),
    path('clients/ajouter/',Ajouter_Client,name='Ajouter_Client'),
    path('clients/modifier/<int:id>/', modifier_client, name='modifier_client'),
    path('clients/desactiver/<int:id>/',desactiver_client,name='desactiver_client'),
    path(
    'clients/activer/<int:id>/',
    activer_client,
    name='activer_client'
),
path(
    'medicaments/ajouter/',
    ajouter_medicament,
    name='ajouter_medicament'
),
path(
    'medicaments/modifier/<int:id>/',
    modifier_medicament,
    name='modifier_medicament'
),
path(
    'medicaments/desactiver/<int:id>/',
    desactiver_medicament,
    name='desactiver_medicament'
),
path(
    'medicaments/activer/<int:id>/',
    activer_medicament,
    name='activer_medicament'
),
path(
    'commandes/<int:id>/statut/',
    modifier_statut_commande,
    name='modifier_statut_commande'
),
path(
    'client/dashboard/',
    client_dashboard,
    name='client_dashboard'
),
path(
    "register/",
    register_view,
    name="register"
),
path(
    "demandes-inscription/",
    demandes_inscription,
    name="demandes_inscription"
),
path(
    "demandes-inscription/<int:pk>/accepter/",
    accepter_demande_frontend,
    name="accepter_demande_frontend"
),

path(
    "demandes-inscription/<int:pk>/refuser/",
    refuser_demande_frontend,
    name="refuser_demande_frontend"
),
 path(
        'panier/ajouter/',
        ajouter_panier,
        name='ajouter_panier'
    ),

    path(
        'panier/',
        panier,
        name='panier'
    ),

    path(
        'panier/retirer/<int:medicament_id>/',
        retirer_panier,
        name='retirer_panier'
    ),

    path(
        'panier/modifier/<int:medicament_id>/',
        modifier_quantite_panier,
        name='modifier_quantite_panier'
    ),

    path(
        'panier/vider/',
        vider_panier,
        name='vider_panier'
    ),

    path(
        'commande/valider/',
        valider_commande,
        name='valider_commande'
    ),
    path(
    'mes_commandes/',
    client_commandes,
    name='client_commandes'
),
path(
    'acheteur/stock/',
    acheteur_stock,
    name='acheteur_stock'
),
path(
    'acheteur/stock/ajouter/',
    ajouter_stock_frontend,
    name='ajouter_stock_frontend'
),
path(
    'acheteur/stock/modifier/<int:pk>/',
    modifier_stock_frontend,
    name='modifier_stock_frontend'
),

path(
    'acheteur/stock/supprimer/<int:pk>/',
    supprimer_stock_frontend,
    name='supprimer_stock_frontend'
),
path(
    'stock-acheteurs/',
    stock_acheteurs,
    name='stock_acheteurs'
),

]