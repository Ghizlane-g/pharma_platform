from django.urls import path

from .views import (
    creer_demande,
    demandes_list,
    accepter_demande,
    refuser_demande
)


urlpatterns = [

    path(
        'inscription/',
        creer_demande,
        name='creer_demande'
    ),

    path(
        'admin/demandes/',
        demandes_list,
        name='demandes_list'
    ),
    path(
    'admin/demandes/<int:pk>/accepter/',
    accepter_demande,
    name='accepter_demande'
),

path(
    'admin/demandes/<int:pk>/refuser/',
    refuser_demande,
    name='refuser_demande'
),

]