from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import ClientViewSet, create_client

router = DefaultRouter()

router.register(
    r'clients',
    ClientViewSet,
    basename='clients'
)

urlpatterns = [
    path(
        'clients/create/',
        create_client,
        name='create_client'
    ),
]

urlpatterns += router.urls