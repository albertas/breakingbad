from django_filters import rest_framework as filters

from breakingbadapi_task.models import Character


class CharacterFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    status = filters.CharFilter(field_name="status", lookup_expr="icontains")
    birthday = filters.CharFilter(field_name="birthday", lookup_expr="icontains")
    occupation = filters.CharFilter(field_name="occupation__title", lookup_expr="icontains")

    class Meta:
        model = Character
        fields = ["name", "status", "birthday", "occupation"]
