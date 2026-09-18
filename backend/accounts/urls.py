from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, statistics, accounts_list, clients_list, commandes_list, medicaments_list, current_user,client_medicaments_list,mon_stock,ajouter_stock ,modifier_stock,supprimer_stock,liste_medicaments_acheteur,stock_acheteurs

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('users/me/', current_user, name='current_user'),
    path('', include(router.urls)),
    path('statistics/', statistics, name='statistics'),
    path('accounts/', accounts_list, name='accounts_list'),
    path('clients/', clients_list, name='clients_list'),
    path('commandes/', commandes_list, name='commandes_list'),
    path('medicaments/', medicaments_list, name='medicaments_list'),
    path('client/medicaments/', client_medicaments_list, name='client_medicaments_list'),
    path(
    'acheteur/mon-stock/',
    mon_stock,
    name='mon_stock'
),
path(
    'acheteur/mon-stock/ajouter/',
    ajouter_stock,
    name='ajouter_stock'
),
path(
    'acheteur/mon-stock/<int:pk>/',
    modifier_stock,
    name='modifier_stock'
),
path(
    'acheteur/mon-stock/<int:pk>/supprimer/',
    supprimer_stock,
    name='supprimer_stock'
),
path(
    'acheteur/medicaments/',
    liste_medicaments_acheteur,
    name='liste_medicaments_acheteur'
),
path(
    'admin/stock-acheteurs/',
    stock_acheteurs,
    name='stock_acheteurs'
),
]