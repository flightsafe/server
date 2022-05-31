from rest_framework import serializers

from .models import BookingRecord


class BookingRecordSerializer(serializers.ModelSerializer):
    plane_name = serializers.StringRelatedField()

    class Meta:
        model = BookingRecord
        fields = "__all__"


class BookingRecordOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingRecord
        exclude = ["user"]
