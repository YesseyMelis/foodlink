from uuid import uuid4

from django.db import models

from foodlink_back.apps.authentication.models import CoreUser
from foodlink_back.apps.common.models import Product
from foodlink_back.apps.core.models import Address
from foodlink_back.apps.order.enums import Statuses
from foodlink_back.apps.order.interfaces import OrderStatuses


class Order(models.Model):
    cook = models.ForeignKey(CoreUser, on_delete=models.PROTECT, related_name='cook_orders')
    token = models.CharField(max_length=36, unique=True, blank=True)
    status = models.CharField(max_length=32, default=Statuses.COLLECTION.value, choices=OrderStatuses.choices)
    prev_status = models.CharField(max_length=32, default=Statuses.COLLECTION.value, choices=OrderStatuses.choices)
    delivery_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, related_name='orders')
    user = models.ForeignKey(CoreUser, on_delete=models.PROTECT, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="orders")
    total = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('id',)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = str(uuid4())

        update_fields = kwargs.get('update_fields', None)
        if update_fields:
            if 'status' in update_fields and self.pk:
                obj = Order.objects.values('status').get(pk=self.pk)
                if obj and obj['status'] != self.status:
                    self.prev_status = obj['status']
                    if isinstance(update_fields, tuple):
                        update_fields = list(update_fields + ('prev_status',))
                    else:
                        update_fields.append('prev_status')
        return super(Order, self).save(*args, update_fields=update_fields)


class OrderStatus(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, related_name='statues')
    status = models.CharField(max_length=32, default=Statuses.COLLECTION.value, choices=OrderStatuses.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статус заказа'
