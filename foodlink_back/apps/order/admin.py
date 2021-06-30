from django.contrib import admin

from foodlink_back.apps.order.models import Order, OrderStatus

admin.site.register(Order)
admin.site.register(OrderStatus)
