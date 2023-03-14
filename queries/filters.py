import django_filters
from cafe.models import Order


class OrderFilter(django_filters.FilterSet):
    registered_date = django_filters.DateTimeFilter()
    start_date = django_filters.DateFilter(
        field_name="registered_date", lookup_expr="gte"
    )
    end_date = django_filters.DateFilter(
        field_name="registered_date", lookup_expr="lte"
    )

    # class Meta:
    #     model = Order
    #     fields = ['registered_date']

    class Meta:
        """Meta Class"""

        model = Order
        fields = {"registered_date": ["lte", "gte"]}
