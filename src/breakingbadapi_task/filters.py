from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django_filters import rest_framework as filters
from rest_framework import serializers

from breakingbadapi_task.models import Character, Location


class CharacterOrderingFilter(filters.OrderingFilter):
    def filter_queryset(self, request, queryset, view):
        order_by = request.query_params.get("orderBy") or "name"
        ascending = request.query_params.get("ascending") or "1"

        if order_by not in ["name", "birthday"]:
            return queryset

        if ascending == "0":
            order_by = f"-{order_by}"

        return queryset.order_by(order_by)


class CharacterFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    status = filters.CharFilter(field_name="status", lookup_expr="icontains")
    birthday = filters.CharFilter(field_name="birthday", lookup_expr="icontains")
    occupation = filters.CharFilter(field_name="occupation__title", lookup_expr="icontains")

    orderBy = filters.CharFilter(
        method="do_nothing",
        help_text="Field name to order by: name or birthday",
    )
    ascending = filters.CharFilter(
        method="do_nothing", help_text="Ordering order: use 0 for descending and 1 for ascending"
    )

    class Meta:
        model = Character
        fields = ["name", "status", "birthday", "occupation"]

    def do_nothing(self, queryset, name, value):
        return queryset


class LocationFilter(filters.FilterSet):
    distance = filters.CharFilter(
        method="filter_by_distance",
        help_text='Filter by distance in KMs from a given point ("latitude" and "longitude" params)',
    )
    latitude = filters.CharFilter(
        method="check_if_all_needed_values_are_provided",
        help_text='"latitude" of a given point to filter by distance from',
    )
    longitude = filters.CharFilter(
        method="check_if_all_needed_values_are_provided",
        help_text='"longitude" of a given point to filter by distance from',
    )
    datetime_from = filters.CharFilter(
        method="filter_datetime_from",
        help_text="From when Location records have to be provided e.g. 2020-11-10T10:00:00.00Z",
    )
    datetime_until = filters.CharFilter(
        method="filter_datetime_until",
        help_text="Until when Location records have to be provided e.g. 2020-11-10T24:00:00.00Z",
    )

    class Meta:
        model = Location
        fields = [
            "character",
            "timestamp",
            "distance",
            "latitude",
            "longitude",
            "datetime_from",
            "datetime_until",
        ]

    def check_if_all_needed_values_are_provided(self, queryset, *args, **kwargs):
        if (
            "latitude" not in self.data
            or "longitude" not in self.data
            or "distance" not in self.data
        ):
            message = (
                'You have to provide "latitude" and "longitude" of a point '
                'to filter by "distance" from it.'
            )
            raise serializers.ValidationError(message)
        return queryset

    def filter_by_distance(self, queryset, name, value):
        self.check_if_all_needed_values_are_provided(queryset)

        distance = float(value)
        latitude = float(self.data["latitude"])
        longitude = float(self.data["latitude"])
        ref_point = Point(latitude, longitude)

        return (
            queryset.filter(point__distance_lte=(ref_point, D(km=distance)))
            .annotate(distance=Distance("point", ref_point))
            .order_by("distance")
        )

    def filter_datetime_from(self, queryset, name, value):
        return queryset.filter(timestamp__gt=value)

    def filter_datetime_until(self, queryset, name, value):
        return queryset.filter(timestamp__lt=value)
