from django.core.management.base import BaseCommand
from django.utils import timezone

from orders.models import Order


class Command(BaseCommand):
    help = 'Check Order Expired Status'

    def handle(self, *args, **options):
        now = timezone.now()
        for row in Order.objects.filter(status='pending', expired_at__lte=now):
            row.status = 'expired'
            row.save()
            row.account.set_free()
            self.stdout.write(f'{row.account} has set to free')
