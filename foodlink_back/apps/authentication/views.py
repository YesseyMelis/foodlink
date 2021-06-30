import logging

from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from foodlink_back.apps.authentication.mixins import MethodMatchingViewSetMixin
from foodlink_back.apps.authentication.models import CoreUser, PhoneNumber, UserPin
from foodlink_back.apps.authentication.serializers import AuthenticateSerializer, SendOTPSerializer, \
    VerifyOTPSerializer, ValidatePhoneSerializer, PinMakeSerializer, VerifyPinSerializer, CoreUserSerializer, \
    CoreUserUpdateSerializer, ExistsSerializer, PinSerializer, ErrorResponseSerializer, AuthTokenSerializer

logger = logging.getLogger(__name__)


class RegistrationAPIView(generics.CreateAPIView):
    queryset = CoreUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = AuthenticateSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserDetailsView(generics.RetrieveAPIView):
    queryset = CoreUser.objects.all()
    serializer_class = CoreUserSerializer
    lookup_field = 'phone'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserUpdateProfileView(generics.UpdateAPIView):
    queryset = CoreUser.objects.all()
    serializer_class = CoreUserUpdateSerializer
    parser_classes = (FormParser, MultiPartParser, FileUploadParser)
    lookup_field = 'phone'
    http_method_names = ('put',)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        logger.info("User updated with data {}".format(request.data))
        return Response(CoreUserSerializer(instance).data)


class AuthenticateViewSet(MethodMatchingViewSetMixin, viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = CoreUser.objects.all()
    serializer_class = AuthenticateSerializer
    action_serializers = {
        "send_otp": SendOTPSerializer,
        "verify_otp": VerifyOTPSerializer,
        "validate_phone": ValidatePhoneSerializer,
        "pin": PinMakeSerializer,
        "verify_pin": VerifyPinSerializer,
    }
    http_method_names = ('post', 'put')

    @action(
        methods=["post"],
        detail=False
    )
    def send_otp(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data.get("phone")[0]
        phone_number.send_otp()
        return Response(self.get_serializer().data)

    @action(methods=["post"], detail=False)
    def verify_otp(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = self.get_queryset().filter(phone=serializer.validated_data.get('phone')).first()
            if user:
                refresh = RefreshToken.for_user(user)
                ser = AuthTokenSerializer(data={
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                })
                ser.is_valid(raise_exception=True)
                return Response(ser.data)
        ser = ErrorResponseSerializer(data={'error': 'Invalid otp or phone.'})
        ser.is_valid(raise_exception=True)
        return Response(ser.data, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["put"], detail=False)
    def validate_phone(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data.get("phone")
        exists = self.get_queryset().filter(phone=phone).exists()
        ser = ExistsSerializer(data={"exists": exists})
        ser.is_valid(raise_exception=True)
        return Response(ser.data)

    @action(methods=["post"], detail=True)
    def pin(self, request, *args, **kwargs):
        instance = self.get_object()
        pin = UserPin(
            user=instance
        )
        serializer = self.get_serializer(pin, data=request.data)
        if serializer.is_valid():
            pin = serializer.save()
            logger.info("Create pin code for user {}".format(pin))
            return Response({}, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["put"], detail=True)
    def verify_pin(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pin = serializer.validated_data.get("pin")
        if self.get_object().pin_code.pin != pin:
            ser = PinSerializer(data={"status": False})
            ser.is_valid(raise_exception=True)
            return Response(ser.data, status=status.HTTP_400_BAD_REQUEST)
        ser = PinSerializer(data={"status": True})
        ser.is_valid(raise_exception=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    @action(methods=["put"], detail=True, permission_classes=(IsAuthenticated,), serializer_class=None)
    def change_role(self, request, *args, **kwargs):
        instance: CoreUser = self.get_object()
        is_cook = not instance.is_cook
        instance.is_cook = is_cook
        instance.save(update_fields=["is_cook"])
        return Response(CoreUserSerializer(instance).data)
