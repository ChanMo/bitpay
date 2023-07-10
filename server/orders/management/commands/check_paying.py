import datetime
import time

from django.utils import timezone
from django.core.management.base import BaseCommand

from accounts.models import Account
from orders.models import Order, OrderLine
from utils import tron


class Command(BaseCommand):
    help = 'Check TRC20 Recharge Event'

    def add_arguments(self, parser):
        parser.add_argument('--start', help='input isoformat')

    def get_accounts(self):
        return [i.address for i in Account.objects.filter(is_free=False)]

    def handle(self, *args, **options):
        if options['start']:
            start_at = datetime.datetime.fromisoformat(options['start'])
            start_at = timezone.make_aware(start_at)
        else:
            start_at = datetime.now()
        end_at = start_at - datetime.timedelta(minutes=1)

        accounts = self.get_accounts()

        while start_at > end_at:
            self.stdout.write('start_at: {}'.format(start_at))
            transactions = tron.get_usdt_transaction(int(start_at.timestamp() * 1000))

            if not transactions:
                self.stdout.write('no transactions found')
                break

            self.stdout.write(
                'transactions total: {}'.format(len(transactions)))

            for row in transactions:
                address = row['result']['to']
                if address in accounts and not OrderLine.objects.filter(txid=row['transaction']).exists():
                    value = int(row['result']['value'])
                    self.stdout.write(f'address: {address}, value: {value}')
                    res = tron.get_transaction_info(row['transaction'])
                    order = Order.objects.live().filter(account=address).first()
                    if not order:
                        continue

                    order.orderline_set.create(
                        sender=row['result']['from'],
                        value = value,
                        txid = row['transaction'],
                        data=res
                    )

                    
            start_at = datetime.datetime.fromtimestamp(
                transactions[-1]['timestamp']/1000)
            start_at = timezone.make_aware(start_at)

            time.sleep(5)
