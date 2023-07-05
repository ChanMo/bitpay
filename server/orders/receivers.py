from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Sum
from .models import Order, OrderLine


@receiver(post_save, sender=Order)
def set_account_status(sender, instance=None, created=False, **kwargs):
    if not created:
        return
    account = instance.account
    account.is_free = False
    account.save()
    

@receiver(post_save, sender=OrderLine)
def check_order_status(sender, instance=None, created=False, **kwargs):
    if not created:
        return
    order = instance.order
    value = order.orderline_set.aggregate(Sum('value')).get('value__sum')
    if value < order.value:
        return
    
    order.status = 'success'
    order.save()
