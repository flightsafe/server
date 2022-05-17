from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from django.shortcuts import render
from rest_framework.parsers import MultiPartParser

from .serializers import MaintenanceRecordSerializer, MaintenanceRecordItemSerializer, PlaneSerializer, \
    PlaneDetailSerializer, MaintenanceRecordDetailSerializer
from .models import Plane, MaintenanceRecord, MaintenanceRecordItem


# Create your views here.
class PlaneViewSet(viewsets.ModelViewSet):
    queryset = Plane.objects.all()
    serializer_class = PlaneSerializer
    filter_backends = [DjangoFilterBackend]
    parser_classes = [MultiPartParser]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PlaneDetailSerializer
        return super().get_serializer_class()


class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRecord.objects.all()
    serializer_class = MaintenanceRecordSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return MaintenanceRecordDetailSerializer
        return super().get_serializer_class()


class MaintenanceRecordItemViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRecordItem.objects.all()
    serializer_class = MaintenanceRecordItemSerializer
