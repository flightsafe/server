from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions

from booking.models import BookingRecord
from booking.serializers import BookingRecordSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = BookingRecord.objects.order_by("id").all()
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = BookingRecordSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['plane']

    def create(self, request, *args, **kwargs):
        request.data["user"] = request.user.pk
        return super().create(request, *args, **kwargs)
