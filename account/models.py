from django.db import models

from product.models import Size, Product

class User(models.Model):
    email          = models.CharField(max_length=50, unique=True)
    password       = models.CharField(max_length=200)
    preferred_size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'users'

class Address(models.Model):
    receiver     = models.CharField(max_length=45)
    phone_number = models.CharField(max_length=45)
    address      = models.CharField(max_length=200)
    is_default   = models.BooleanField(default=False)
    user         = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'addresses'

class Wishlist(models.Model):
    is_whished = models.BooleanField(default=True)
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    product    = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'wishlists'



