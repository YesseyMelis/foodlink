from django.db import models

from foodlink_back.apps.authentication.models import CoreUser


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    is_active = models.BooleanField(default=True)
    photo = models.ImageField(upload_to='product_photos', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    weight = models.FloatField(default=0)

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюдо'

    def __str__(self):
        return self.name


class CookMenu(models.Model):
    cook = models.ForeignKey(CoreUser, on_delete=models.SET_NULL, null=True, related_name="menu")
    foods = models.ManyToManyField(Product, blank=True, related_name="menu")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Меню повара'
        verbose_name_plural = 'Меню повара'


class CookRating(models.Model):
    cook = models.ForeignKey(CoreUser, on_delete=models.SET_NULL, null=True, related_name="rating")
    client = models.ForeignKey(CoreUser, on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Рейтинг повара'
        verbose_name_plural = 'Рейтинг повара'
