from django.db import models
from uuid import uuid4


class Transactions(models.Model):
    _id = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey('users.User', null=False,
                             on_delete=models.CASCADE)

    balance = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True, default=0)
    deposit = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True, default=0)
    withdrawal = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True, default=0)
    Total_earning = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True, default=0)

    def __str__(self):
        return self._id


class AdminHistory(models.Model):
    _id = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True, default=0)
    isapproved = models.BooleanField(default=False)
    type = models.CharField(max_length=200, null=True, blank=True)
    package = models.CharField(max_length=200, null=True, blank=True)
    wallet_address = models.CharField(max_length=200, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
