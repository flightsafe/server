import calendar
from datetime import timedelta

from dateutil import parser

from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.timezone import make_aware
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from booking.models import BookingRecord
from booking.serializers import BookingRecordSerializer, BookingRecordOptionSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = BookingRecord.objects.order_by("id").all()
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = BookingRecordSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['plane', "start_time"]

    def get_serializer_class(self):
        if self.action == "metadata":
            return BookingRecordOptionSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = super().get_queryset()
        if "time" in self.request.query_params:
            current_time_str = self.request.query_params.get("time")
            current_time = make_aware(parser.parse(current_time_str))
            _, num_days = calendar.monthrange(current_time.year, current_time.month)
            first_day_of_the_month = current_time.replace(day=1)
            start_time = (first_day_of_the_month - timedelta(days=2)).replace(day=1)
            end_time = first_day_of_the_month + timedelta(days=num_days + 20)
            queryset = queryset.filter(Q(start_time__lte=end_time) & Q(start_time__gte=start_time))
        return queryset

    def create(self, request, *args, **kwargs):
        request.data["user"] = request.user.pk
        request.data["user"] = User.objects.first().pk
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
