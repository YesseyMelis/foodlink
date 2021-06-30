from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from foodlink_back.apps.authentication.models import CoreUser, UserOtp, PhoneNumber, UserPin
from foodlink_back.apps.common.serializers import ProductSerializer
from foodlink_back.apps.core.models import Address
from foodlink_back.apps.core.serializers import AddressSerializer


class AuthenticateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = CoreUser
        fields = ('phone', 'password', 'token')

    def create(self, validated_data):
        if not PhoneNumber.objects.filter(phone=validated_data.get('phone')).exists():
            PhoneNumber.objects.create(phone=validated_data.get('phone'))
        return CoreUser.objects.create_user(**validated_data)


class SendOTPSerializer(serializers.Serializer):
    success = serializers.BooleanField(read_only=True, default=True)
    phone = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs.get("phone", None) is not None:
            attrs["phone"] = PhoneNumber.objects.get_or_create(phone=attrs["phone"])
        return attrs


class VerifyOTPSerializer(serializers.Serializer):
    success = serializers.BooleanField(read_only=True, default=True)
    phone = serializers.CharField(write_only=True)
    otp_code = serializers.CharField(write_only=True)

    def validate(self, attrs):
        phone = PhoneNumber.objects.filter(phone=attrs.get("phone")).first()
        if phone:
            otp = phone.verify_otp(attrs['otp_code'])
            if otp is None:
                raise ValidationError({
                    "otp_code": "Enter a valid otp code"
                })
        else:
            raise ValidationError({
                "phone": "Phone number not exists"
            })
        return attrs


class ValidatePhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(write_only=True)
    exists = serializers.BooleanField(read_only=True)


class PinMakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPin
        fields = ("pin",)


class VerifyPinSerializer(serializers.Serializer):
    pin = serializers.CharField()


class CoreUserSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    products = serializers.SerializerMethodField()

    class Meta:
        model = CoreUser
        fields = ["id", "phone", "first_name", "last_name", "address", "is_cook", "payment_method", "products"]

    def get_products(self, obj):
        if obj.is_cook:
            products = obj.menu.first().foods.all()
            serializer = ProductSerializer(products, many=True)
            return serializer.data
        return []


class CoreUserUpdateSerializer(serializers.ModelSerializer):
    address = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    avatar = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = CoreUser
        fields = ["first_name", "last_name", "address", "payment_method", "avatar"]

    def update(self, instance, validated_data):
        if validated_data.get("address", None):
            validated_data["address"] = Address.objects.create(name=validated_data["address"])
        return super().update(instance, validated_data)


class ExistsSerializer(serializers.Serializer):
    exists = serializers.BooleanField()


class PinSerializer(serializers.Serializer):
    status = serializers.BooleanField()


class ErrorResponseSerializer(serializers.Serializer):
    error = serializers.CharField()


class AuthTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
