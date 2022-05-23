from rest_framework import serializers
from .models import BookingRecord


class BookingRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingRecord
        fields = "__all__"
