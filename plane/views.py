from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from .serializers import MaintenanceRecordSerializer, MaintenanceRecordItemSerializer, PlaneSerializer
from .models import Plane, MaintenanceRecord, MaintenanceRecordItem


# Create your views here.
class PlaneViewSet(viewsets.ModelViewSet):
    queryset = Plane.objects.all()
    serializer_class = PlaneSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [""]


class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRecord.objects.all()
    serializer_class = MaintenanceRecordSerializer


class MaintenanceRecordItemViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRecordItem.objects.all()
    serializer_class = MaintenanceRecordItemSerializer