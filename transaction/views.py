from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions

from .models import TransactionInfo
from .serializers import TransactionInfoSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = TransactionInfo.objects.order_by("id").all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TransactionInfoSerializer
    filter_backends = [DjangoFilterBackend]
