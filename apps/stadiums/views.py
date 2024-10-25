from datetime import date, time

from django.db.models import Q
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos.point import Point
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import ListAPIView

from apps.stadiums.filters import StadiumFilter
from apps.stadiums.models import Stadium
from apps.stadiums.serializers import StadiumSerializer


class StadiumsListAPI(ListAPIView):
    serializer_class = StadiumSerializer
    queryset = Stadium.objects.filter(deleter__isnull=True)
    filterset_class = StadiumFilter
    authentication_classes = ()
    permission_classes = ()

    def get_queryset(self):
        location = self.request.query_params.get('location', None) # 'longitude,latitude'

        date = self.request.query_params.get('date', None)
        start_time = self.request.query_params.get('start_time', None)
        end_time = self.request.query_params.get('end_time', None)

        if all((date, start_time, end_time)):
            self.queryset = self.queryset.exclude(
                Q(bookings__date=date) & Q(bookings__start_time__lt=end_time) & Q(bookings__end_time__gt=start_time)
            )

        if location:
            lon, lat = map(float, location.split(','))
            user_location = Point(lon, lat, srid=4326)

            # Filter and annotate distance
            self.queryset = Stadium.objects.annotate(
                distance=Distance('location', user_location)
            ).order_by('distance')

        return self.queryset.prefetch_related("images")

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='location',
                location='query',
            ),
            OpenApiParameter(
                name='date',
                location='query',
                type=date,
            ),
            OpenApiParameter(
                name='start_time',
                location='query',
                type=time,
            ),
            OpenApiParameter(
                name='end_time',
                location='query',
                type=time,
            ),
        ],
        request=StadiumSerializer,
        responses={StadiumSerializer()},
        tags=['Stadiums'],
    )
    def get(self, request, *args, **kwargs):
        return super(StadiumsListAPI, self).get(request, *args, **kwargs)