from decimal import Decimal

from django.db.models import Q
from django_filters import FilterSet, filters

from foodlink_back.apps.authentication.models import CoreUser
from foodlink_back.apps.common.models import Product


class CookListFilter(FilterSet):
    profile_description = filters.CharFilter()
    address = filters.CharFilter(method="filter_by_address")
    name = filters.CharFilter(method="filter_by_name")

    class Meta:
        model = CoreUser
        fields = []

    def filter_by_address(self, qs, name, value):
        return qs.filter(address__name__icontains=value)

    def filter_by_name(self, qs, name, value):
        return qs.filter(Q(first_name__icontains=value) | Q(last_name__icontains=value))


class ExchangeFilter(FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    address = filters.CharFilter(method="filter_by_address")
    price = filters.NumberFilter(method="filter_by_price")
    weight = filters.NumberFilter()

    class Meta:
        model = Product
        fields = []

    def filter_by_address(self, qs, name, value):
        return qs.filter(menu__cook__address__name__icontains=value)

    def filter_by_price(self, qs, name, value):
        return qs.filter(price=Decimal(value))
