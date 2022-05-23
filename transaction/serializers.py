from rest_framework import serializers

from .models import TransactionInfo


class TransactionInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionInfo
        fields = "__all__"
