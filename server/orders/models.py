import uuid
import datetime
from django.utils import timezone
from django.db import models
from accounts.models import Account


def set_expired_at():
    return timezone.now() + datetime.timedelta(minutes=10)

class OrderManager(models.Manager):
    def live(self):
        now = timezone.now()
        return self.filter(created_at__lte=now, expired_at__gte=now)

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failure', 'Failure'),
        ('expired', 'Expired')
    )
    number = models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True)
    user = models.CharField(max_length=200, db_index=True)
    email = models.EmailField(blank=True, null=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, to_field='address')
    value = models.IntegerField(default=0)
    status = models.CharField(max_length=50, default='pending', choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(default=set_expired_at)
    objects = OrderManager

    def __str__(self):
        return str(self.number)

    class Meta:
        ordering = ['-created_at']



class OrderLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    txid = models.CharField(max_length=100, unique=True)
    sender = models.CharField(max_length=200)
    value = models.IntegerField(default=0)
    data = models.JSONField(blank=True, default=dict) # Transaction data
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.order.number}-{self.sender}'

    class Meta:
        ordering = ['-created_at']
