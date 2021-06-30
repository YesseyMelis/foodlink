from rest_framework import serializers

from foodlink_back.apps.authentication.serializers import CoreUserSerializer
from foodlink_back.apps.common.serializers import ProductSerializer
from foodlink_back.apps.core.serializers import AddressSerializer
from foodlink_back.apps.order.enums import Statuses
from foodlink_back.apps.order.models import Order, OrderStatus


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('cook', 'product')

    def __init__(self, **kwargs):
        self.user = kwargs.pop('user', None)
        super(OrderCreateSerializer, self).__init__(**kwargs)

    def validate(self, attrs):
        if attrs.get('product', None):
            attrs['total'] = attrs.get('product').price
        attrs['status'] = Statuses.COLLECTION.value
        attrs['prev_status'] = Statuses.COLLECTION.value
        attrs['user'] = self.user
        return attrs


class ChangeOrderStageSerializer(serializers.Serializer):
    status = serializers.CharField()


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = ('status', 'created_at')


class OrderInfoSerializer(serializers.ModelSerializer):
    cook = CoreUserSerializer()
    user = CoreUserSerializer()
    delivery_address = AddressSerializer()
    product = ProductSerializer()
    statuses = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_statuses(self, obj):
        return OrderStatusHistorySerializer(obj.statues.all(), many=True).data
