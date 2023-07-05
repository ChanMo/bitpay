import requests
from django.conf import settings
from django.db import models


class Account(models.Model):
    address = models.CharField(max_length=200, db_index=True, unique=True)
    private_key = models.CharField(max_length=200)
    is_free = models.BooleanField(default=True, help_text='is available for ordering')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.address

    def save(self, *args, **kwargs):
        if self._state.adding:
            r = requests.post(f'{settings.TRON_API}/create_account', timeout=3000)
            res = r.json()
            self.address = res['address']['base58']
            self.private_key = res['privateKey']

        return super().save(*args, **kwargs)

    def set_free(self):
        self.is_free = True
        return self.save()

    class Meta:
        ordering = ['-created_at']


def get_free_account():
    if Account.objects.filter(is_free=True).exists():
        return Account.objects.filter(is_free=True).first()
    return Account.objects.create()
