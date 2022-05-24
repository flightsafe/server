from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser

from .models import Plane, MaintenanceRecord, MaintenanceRecordItem
from .serializers import MaintenanceRecordSerializer, MaintenanceRecordItemSerializer, PlaneSerializer, \
    MaintenanceRecordDetailSerializer


# Create your views here.
class PlaneViewSet(viewsets.ModelViewSet):
    queryset = Plane.objects.all()
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PlaneSerializer
    filter_backends = [DjangoFilterBackend]
    parser_classes = [MultiPartParser]
    filterset_fields = ['name', "description", "id"]
    search_fields = ["name"]


class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRecord.objects.order_by("id").all()
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = MaintenanceRecordSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['plane']
    ordering_fields = ["progress"]
    search_fields = ["name"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return MaintenanceRecordDetailSerializer
        return super().get_serializer_class()


class MaintenanceRecordItemViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRecordItem.objects.all()
    serializer_class = MaintenanceRecordItemSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
