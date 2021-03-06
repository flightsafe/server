from rest_framework import serializers

from .models import Plane, MaintenanceRecord, MaintenanceRecordItem


class MaintenanceRecordSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(read_only=True)
    end_time = serializers.DateTimeField(read_only=True)
    status = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = MaintenanceRecord
        exclude = ["author"]


class MaintenanceRecordItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceRecordItem
        fields = "__all__"


class PlaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plane
        exclude = ["description"]


class PlaneDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plane
        fields = "__all__"


class MaintenanceRecordDetailSerializer(serializers.ModelSerializer):
    items = MaintenanceRecordItemSerializer(many=True, read_only=True)
    start_time = serializers.DateTimeField(read_only=True)
    end_time = serializers.DateTimeField(read_only=True)
    status = serializers.StringRelatedField(read_only=True)
    plane_name = serializers.StringRelatedField(read_only=True, source="plane")

    class Meta:
        model = MaintenanceRecord
        fields = "__all__"


class PlaneDetailSerializer(serializers.ModelSerializer):
    records = MaintenanceRecordSerializer(many=True, read_only=True)

    class Meta:
        model = Plane
        fields = "__all__"
