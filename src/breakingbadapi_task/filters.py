from django_filters import rest_framework as filters

from breakingbadapi_task.models import Character


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
