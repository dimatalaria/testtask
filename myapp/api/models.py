from uuid import uuid4
from django.utils import timezone
from django.db import models

class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    owner_name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=timezone.now)


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    from_account = models.ForeignKey(Account, related_name='outgoing_transactions', on_delete=models.CASCADE)
    to_account = models.ForeignKey(Account, related_name='incoming_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)