from base64 import b32encode
from datetime import datetime, timedelta
from typing import Union

import jwt
from django.conf import settings
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from pyotp import TOTP

from foodlink_back.apps.core.enums import PaymentInterface, PaymentMethods
from foodlink_back.apps.core.models import Address


class DateFixingModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserManager(BaseUserManager):
    def _create_user(self, phone, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not phone:
            raise ValueError('The given email must be set')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)


class CoreUser(AbstractBaseUser, PermissionsMixin):
    nickname = models.CharField(null=True, max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=191, blank=True, null=True)
    last_name = models.CharField(max_length=191, blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_cook = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)

    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        related_name="user",
        null=True
    )

    payment_method = models.CharField(max_length=20, choices=PaymentInterface.choices, default=PaymentMethods.CASH.name)

    avatar = models.ImageField(upload_to='user_avatars', blank=True, null=True)

    profile_description = models.TextField(null=True, blank=True)

    USERNAME_FIELD = 'phone'

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'core_users'

    def __str__(self):
        return self.phone or self.nickname

    @property
    def get_full_name(self):
        return f'{self.last_name} {self.first_name}'

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def token(self):
        """
        Позволяет получить токен пользователя путем вызова user.token, вместо
        user._generate_jwt_token(). Декоратор @property выше делает это
        возможным. token называется "динамическим свойством".
        """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Генерирует веб-токен JSON, в котором хранится идентификатор этого
        пользователя, срок действия токена составляет 1 день от создания
        """
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


class OTPManager(models.Manager):
    def generate_otp(self, **kwargs):
        key = b32encode(bytes(settings.SECRET_KEY[:16], encoding="utf-8"))
        otp = TOTP(key, digits=4)
        otp_code = otp.at(datetime.today(), counter_offset=self.model.EXPIRE)
        instance = self.model(
            otp=otp_code,
            **kwargs
        )
        instance.save()
        return instance

    def verify(self, otp_code, **kwargs):
        key = b32encode(bytes(settings.SECRET_KEY[:16], encoding="utf-8"))
        otp = TOTP(key, digits=4)
        instance = self.filter(verified=False, **kwargs).first()
        if bool(
            otp.verify(otp_code, datetime.today(), valid_window=self.model.EXPIRE)
            and instance is not None
            and instance.otp == otp_code
        ):
            instance.verified = True
            instance.save(update_fields=["verified"])
            return instance
        return None


class UserOtp(DateFixingModel):
    otp = models.CharField(max_length=6)
    phone = models.ForeignKey("PhoneNumber", on_delete=models.CASCADE, related_name="otps")
    verified = models.BooleanField(default=False)

    EXPIRE = 60

    objects = OTPManager()

    class Meta:
        verbose_name = 'ОТП коды'
        verbose_name_plural = 'ОТП коды'
        db_table = 'user_otp'

    def __str__(self) -> str:
        return "%s - verified: %s" % (
            self.otp,
            str(self.verified)
        )


class PhoneNumber(DateFixingModel):
    phone = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Phone number"
        verbose_name_plural = "Phone number"

    def send_otp(self) -> models.Model:
        otp = self.otps.generate_otp(
            phone=self,
        )
        # create_otp_sms(otp)
        return otp

    def verify_otp(self, otp_code: str) -> Union[None, models.Model]:
        otp = self.otps.verify(
            otp_code,
            phone=self
        )
        return otp


class UserPin(models.Model):
    user = models.OneToOneField(CoreUser, related_name="pin_code", on_delete=models.CASCADE)
    pin = models.CharField(max_length=6, blank=True)

    class Meta:
        verbose_name = "Пин код пользователя"
        verbose_name_plural = "Пин код пользователя"
