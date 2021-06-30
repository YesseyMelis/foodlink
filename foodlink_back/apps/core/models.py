from django.db import models


class Address(models.Model):
    name = models.CharField("Адрес", max_length=200)
    latitude = models.CharField(max_length=20, null=True, blank=True)
    longitude = models.CharField(max_length=20, null=True, blank=True)
    floor = models.IntegerField(null=True)
    office = models.IntegerField(null=True)

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адрес"

    def __str__(self):
        return self.name
