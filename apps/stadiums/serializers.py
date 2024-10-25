from django.contrib.gis.geos.point import Point
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.stadiums.models import Stadium


class PointField(serializers.Field):
    def to_representation(self, value):
        return value.coords

    def to_internal_value(self, data):
        if not isinstance(data, (tuple, list)):
            raise serializers.ValidationError(_("Invalid point."))
        return Point(data)


class DistanceField(serializers.Field):
    def to_representation(self, value):
        return value.km


class ImageSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    stadium = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=Stadium.objects.all()
    )
    image = serializers.ImageField()


class StadiumSerializer(serializers.Serializer):
    id  = serializers.UUIDField(read_only=True)
    name = serializers.CharField()
    address = serializers.CharField(allow_null=True, allow_blank=True, max_length=255)
    location = PointField()
    contacts = serializers.JSONField(allow_null=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    distance = DistanceField(read_only=True, default=None)
    images = ImageSerializer(many=True, read_only=True)

    def create(self, validated_data):
        return Stadium.objects.create(**validated_data)
