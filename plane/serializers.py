from rest_framework import serializers, viewsets, routers
from .models import Plane, MaintenanceRecord, MaintenanceRecordItem


class MaintenanceRecordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MaintenanceRecord
        fields = "__all__"


class MaintenanceRecordItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MaintenanceRecordItem
        fields = "__all__"


class PlaneSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Plane
        fields = "__all__"
