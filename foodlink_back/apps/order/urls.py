from django.urls import path

from foodlink_back.apps.order.views import OrderView, ChangeOrderStageView, OrderInfoView, MyOrdersView

urlpatterns = [
    path('my_orders/', MyOrdersView.as_view(), name='my-orders-list'),
    path('create/', OrderView.as_view(), name='order-create'),
    path('stage/<str:token>/change/', ChangeOrderStageView.as_view(), name='order-change-status'),
    path('<str:token>/info/', OrderInfoView.as_view(), name='order-info'),
]
app_name = 'order'
