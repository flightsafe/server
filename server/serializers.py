from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField(source="username")

    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True}
        }