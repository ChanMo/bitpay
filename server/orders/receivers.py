import requests
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Sum
from django.conf import settings
from .models import Order, OrderLine
from .serializers import OrderSerializer


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

    # send notify
    if not settings.PAYMENT_RESULT_NOTIFY:
        return
    try:
        r = requests.post(
            settings.PAYMENT_RESULT_NOTIFY,
            json = {
                'order': OrderSerializer(order).data,
                'event': 'paid'
            },
            timeout=300)
        print(r.json())
    except Exception as e:
        print(e)
