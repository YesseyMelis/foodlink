from django.urls import path

from foodlink_back.apps.core.views import AddressView, CookListView, ExchangeView

urlpatterns = [
    path('address/create/', AddressView.as_view(), name='address-create'),
    path('cooks/', CookListView.as_view(), name='cooks_list'),
    path('exchange/', ExchangeView.as_view(), name='exchange_list'),
]

app_name = 'core'
