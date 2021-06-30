from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from foodlink_back.apps.authentication.models import CoreUser
from foodlink_back.apps.common.models import Product
from foodlink_back.apps.core.filters import CookListFilter, ExchangeFilter
from foodlink_back.apps.core.models import Address
from foodlink_back.apps.core.serializers import AddressSerializer, CookListSerializer, ExchangeSerializer


class AddressView(generics.CreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = (AllowAny,)


class CookListView(generics.ListAPIView):
    queryset = CoreUser.objects.filter(is_cook=True)
    serializer_class = CookListSerializer
    filterset_class = CookListFilter
    permission_classes = (AllowAny,)
    filter_backends = [DjangoFilterBackend, SearchFilter]


class ExchangeView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ExchangeSerializer
    filterset_class = ExchangeFilter
    permission_classes = (AllowAny,)
    filter_backends = [DjangoFilterBackend, SearchFilter]
