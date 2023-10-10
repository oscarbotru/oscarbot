from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=255, blank=True, null=True)


class Product(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(decimal_places=8, max_digits=12)
