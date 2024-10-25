from django_filters import rest_framework as filters

from apps.bookings.models import Booking


class BookingFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="stadium__name", lookup_expr='icontains')
    class Meta:
        model = Booking
        fields = {
            "status": ["exact"],
            "date": ["gte", "lte", "exact"],
            "start_time": ["gte", "lte"],
            "end_time": ["lte", "gte"],
        }