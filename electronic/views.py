from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from .models import Network
from .permissions import IsActiveEmployee
from .serializers import NetworkSerializer


class NetworkViewSet(viewsets.ModelViewSet):
    """
    Набор представлений CRUD для модели поставщика.
    """
    queryset = Network.objects.all()
    serializer_class = NetworkSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['country']
    permission_classes = [IsActiveEmployee]
