from django.db import models
from simple_history.models import HistoricalRecords


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, related_name='stores', on_delete=models.CASCADE, blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class PromoCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(default='None')
    discount_percent = models.PositiveIntegerField(default=0)
    expiration_date = models.DateField()
    is_active = models.BooleanField(default=True)
    store = models.ForeignKey(Store, related_name='promo_codes', on_delete=models.CASCADE, blank=True, null=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    history = HistoricalRecords()
    def __str__(self):
        return self.code


