from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    CommandeViewSet,
    creer_commande,
    mes_commandes
)


router = DefaultRouter()

router.register(
    r'commandes',
    CommandeViewSet,
    basename='commandes'
)


urlpatterns = [
    path(
        'creer/',
        creer_commande,
        name='creer_commande'
    ),

    path(
        'mes-commandes/',
        mes_commandes,
        name='mes_commandes'
    ),
]


urlpatterns += router.urls