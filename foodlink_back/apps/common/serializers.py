from rest_framework import serializers

from foodlink_back.apps.common.models import Product, CookMenu


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'photo')


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = CookMenu
        fields = '__all__'
