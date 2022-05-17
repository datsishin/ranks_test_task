from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    price = models.IntegerField()

    def __str__(self):
        return self.name


class Order(models.Model):
    products = models.ForeignKey(Item, on_delete=models.CASCADE)