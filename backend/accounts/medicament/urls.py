from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    MedicamentViewSet,
    create_medicament,
    medicaments_disponibles
)

router = DefaultRouter()

router.register(
    r'medicaments',
    MedicamentViewSet,
    basename='medicaments'
)

urlpatterns = [
    path(
        'medicaments/create/',
        create_medicament,
        name='create_medicament'
    ),
    path(
        'disponibles/',
        medicaments_disponibles,
        name='medicaments_disponibles'
    ),
]

urlpatterns += router.urls