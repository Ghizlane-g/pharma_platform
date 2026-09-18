from django.urls import path
from .views import medicaments_disponibles

urlpatterns = [
    path(
        '',
        medicaments_disponibles,
        name='medicaments_disponibles'
    ),
]