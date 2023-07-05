import requests
from django.db import models
from django.conf import settings
from products.models import Product


class Order(models.Model):
    ORDER_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('done', 'Done'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pay_data = models.JSONField(max_length=100, blank=True, default=dict)
    status = models.CharField(max_length=50, default='pending', choices=ORDER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

    def get_pay_data(self):
        if not self.pay_data:
            res = self.create_pay_data()
            self.pay_data = res
            self.save()
        return self.pay_data
        

    def create_pay_data(self):
        r = requests.post('http://0.0.0.0:5000/', json={
            'user': self.user.username,
            'email': self.user.email,
        }, timeout=300)
        return r.json()

    class Meta:
        ordering = ['-created_at']
