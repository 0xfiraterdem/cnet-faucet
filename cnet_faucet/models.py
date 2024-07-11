from django.db import models
from django.utils import timezone


class FaucetRequest(models.Model):
    id = models.AutoField(primary_key=True)
    wallet_address = models.CharField( max_length=64)
    request_time = models.DateTimeField(default=timezone.now)
