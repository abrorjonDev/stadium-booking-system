from django_filters import rest_framework as filters

from apps.stadiums.models import Stadium


class StadiumFilter(filters.FilterSet):
    class Meta:
        model = Stadium
        fields = {
            'name': ['icontains'],
            'address': ['icontains'],
        }
