from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import AcheteurViewSet, create_acheteur

router = DefaultRouter()

router.register(
    r'acheteurs',
    AcheteurViewSet,
    basename='acheteurs'
)

urlpatterns = [
    path(
        'acheteurs/create/',
        create_acheteur,
        name='create_acheteur'
    ),
]

urlpatterns += router.urls