from django.db import models

from account.models import User, Address
from product.models import ProductSize


class Status(models.Model):
    condition = models.CharField(max_length=45)

    class Meta:
        db_table = 'statuses'

class Bidding(models.Model):
    price        = models.DecimalField(max_digits=10, decimal_places=2)
    create_at    = models.DateTimeField(auto_now_add=True)
    update_at    = models.DateTimeField(auto_now=True)
    deadline     = models.DateTimeField()
    bidding_type = models.BooleanField()
    user         = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product_size = models.ForeignKey(ProductSize, on_delete=models.SET_NULL, null=True)
    status       = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    address      = models.ForeignKey(Address, on_delete=models.CASCADE)

    class Meta:
        db_table = 'biddings'

