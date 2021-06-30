from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from foodlink_back.apps.authentication.serializers import ErrorResponseSerializer
from foodlink_back.apps.order.enums import Statuses
from foodlink_back.apps.order.models import Order, OrderStatus
from foodlink_back.apps.order.serializers import OrderCreateSerializer, ChangeOrderStageSerializer, OrderInfoSerializer


class MyOrdersView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderInfoSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        orders = request.user.orders
        serializer = self.serializer_class(orders, many=True)
        return Response(serializer.data)


class OrderView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, **{"user": request.user})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        OrderStatus.objects.create(order=order, status=Statuses.COLLECTION.value)
        return Response(OrderInfoSerializer(instance=order).data)


class OrderInfoView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderInfoSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'token'


class ChangeOrderStageView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = ChangeOrderStageSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'token'
    http_method_names = ('put',)

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            order_status = serializer.validated_data.get('status')
            order.status = order_status
            order.save(update_fields=['status'])
            OrderStatus.objects.create(order=order, status=order_status)
            return Response(OrderInfoSerializer(instance=order).data)
        ser = ErrorResponseSerializer(data={'error': 'Incorrect status.'})
        ser.is_valid(raise_exception=True)
        return Response(ser.data, status=status.HTTP_400_BAD_REQUEST)
