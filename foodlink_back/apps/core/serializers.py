from django.db.models import Sum
from rest_framework import serializers

from foodlink_back.apps.common.models import Product
from foodlink_back.apps.common.serializers import ProductSerializer
from foodlink_back.apps.core.models import Address
from foodlink_back.apps.authentication.models import CoreUser


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class CookListSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    address = AddressSerializer()
    products = serializers.SerializerMethodField()

    class Meta:
        model = CoreUser
        fields = (
            'id',
            'phone',
            'last_name',
            'first_name',
            'address',
            'avatar',
            'profile_description',
            'rating',
            'products'
        )

    def get_rating(self, obj):
        total_rating = obj.rating.annotate(total_rating=Sum('rating')).values_list('total_rating')
        if total_rating:
            return total_rating[0] / obj.rating.count()
        return 5

    def get_products(self, obj):
        products = obj.menu.first().foods.all()
        serializer = ProductSerializer(products, many=True)
        return serializer.data


class ExchangeSerializer(serializers.ModelSerializer):
    cook = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'photo', 'cook')

    def get_cook(self, obj):
        ser = CookListSerializer(obj.menu.first().cook)
        return ser.data
