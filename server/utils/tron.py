import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

TRX_API = settings.TRON_API

def get_transaction(txid):
    # 查询交易详情
    url = '{}/get_transaction/{}'.format(TRX_API, txid)
    r = requests.get(url, timeout=300)
    return r.json()

def get_transaction_info(txid):
    # 查询交易详情
    url = '{}/get_transaction_info/{}'.format(TRX_API, txid)
    r = requests.get(url, timeout=300)
    return r.json()

def get_usdt_transaction(since):
    # 获取交易记录
    url = f'{TRX_API}/contract/{settings.TRON_USDT}/get_transactions/'
    r = requests.get(url, {'sinceTimestamp':since}, timeout=300)
    if not r.status_code == requests.codes.ok:
        logger.warning(r.status_code)
        logger.warning(r.text)
        return []
    res = r.json()
    return res


def get_balance(address):
    # 获取TRX余额
    url = '{}/get_balance/{}'.format(
        TRX_API, address
    )
    r = requests.get(url, timeout=300)
    return r.json()['balance']


def get_usdt_balance(address):
    # 获取USDT余额
    url = f'{TRX_API}/contract/{settings.TRON_USDT}/get_balance/{address}'
    r = requests.get(url, timeout=300)
    return r.json()['balance']


def send_usdt(to, value, private_key):
    # 发送USDT
    url = f'{TRX_API}/contract/{settings.TRON_USDT}transfer'
    r = requests.post(url, json={
        'private_key': private_key,
        'to': to,
        'value': value
    }, timeout=300)
    res = r.json()
    return res


def send_trx(to, value, private_key):
    # 发送Trx
    url = '{}/send_transfer'.format(TRX_API)
    r = requests.post(url, json={
        'private_key': private_key,
        'to': to,
        'amount': value
    }, timeout=300)
    res = r.json()
    print(res)
    return res

