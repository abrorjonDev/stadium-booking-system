from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from apps.bookings.models import Booking, StatusChoice
from apps.stadiums.serializers import StadiumSerializer


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "date", "start_time", "end_time", "status", "stadium"]
        read_only_fields = "status",

    def validate(self, data):
        date = data.get("date") or self.instance.date
        start_time = data.get("start_time") or self.instance.start_time
        end_time = data.get("end_time") or self.instance.end_time
        stadium = data.get("stadium") or self.instance.stadium

        if start_time > end_time:
            raise serializers.ValidationError(_("Wrong time orderings"))

        bookings_qs = (
            Booking.objects.filter(
                stadium=stadium, status=StatusChoice.CONFIRMED
            ).filter(
                Q(start_time__gt=start_time, start_time__lt=end_time)
                | Q(start_time__lt=end_time, end_time__gt=end_time),
                date=date)
        )
        if self.instance:
            bookings_qs = bookings_qs.exclude(id=self.instance.id)
        if bookings_qs.exists():
            raise serializers.ValidationError(_("Already booked for this time."))

        return data

    def to_representation(self, instance):
        return BookingReadSerializer(instance, context=self.context).data


class BookingReadSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    date = serializers.DateField(read_only=True)
    start_time = serializers.TimeField(read_only=True)
    end_time = serializers.TimeField(read_only=True)
    stadium = StadiumSerializer(read_only=True)
    status = serializers.CharField(read_only=True)
