from django.db import models
from shop.models import *
from auth_user.models import *


class Order(models.Model):
    products = models.ManyToManyField(Product)
    profile = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE)
    object = models.Manager()