from django.contrib.auth.models import User
from django.db import models


class Bonds(models.Model):
    isin = models.CharField(max_length=20, unique=True, null=False)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.isin

    class Meta:
        verbose_name_plural = "Bonds"


class Deals(models.Model):
    buy = models.BooleanField(null=False)
    quantity = models.IntegerField(null=False)
    price_at_the_time = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    time_create = models.DateTimeField(auto_now_add=True)
    bonds = models.ForeignKey('Bonds', on_delete=models.PROTECT, null=False, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    class Meta:
        ordering = ['time_create']
        verbose_name_plural = "Deals"
