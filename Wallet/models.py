from django.db import models
from uuid import uuid4

def hex_uuid():
    return uuid4().hex

# Create your models here.
class Wallet(models.Model):
    STATUS_CHOICES = (
        (0, 'enabled'),
        (1, 'disabled')
    )
    
    id          = models.CharField(max_length=36, null=False, blank=False, primary_key=True, default=uuid4)
    token       = models.CharField(max_length=36, null=False, blank=False, default=hex_uuid)
    owner       = models.CharField(max_length=36, null=False, blank=False)
    status      = models.IntegerField(choices=STATUS_CHOICES, default=0, null=False, blank=False)
    enabled_at  = models.DateTimeField(null=True)
    disabled_at = models.DateTimeField(null=True)
    balance     = models.IntegerField(default=0, null=False, blank=False)
    
    
class WalletTransaction(models.Model):
    id              = models.CharField(max_length=36, null=False, blank=False, primary_key=True, default=uuid4)
    wallet          = models.ForeignKey(Wallet, related_name='transactions', on_delete=models.DO_NOTHING)
    reference_id    = models.CharField(max_length=36, null=False, blank=False, unique=True)
    deposited_at    = models.DateTimeField(null=True)
    withdrawn_at    = models.DateTimeField(null=True)
    amount          = models.IntegerField(null=False, blank=False)