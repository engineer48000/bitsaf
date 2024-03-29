from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4


class User(AbstractUser):

    uuid = models.UUIDField(default=uuid4)
    date_joined = models.DateField(auto_now_add=True)
    referral = models.CharField(max_length=200, null=True, blank=True)
    firstname = models.CharField(max_length=200, null=True, blank=True)
