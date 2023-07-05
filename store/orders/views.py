from django.shortcuts import redirect
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from products.models import Product
from .models import Order


class CheckoutView(LoginRequiredMixin, DetailView):
    queryset = Product.objects.all()
    template_name = 'checkout.html'

    def post(self, *args, **kwargs):
        obj = self.get_object()
        order = Order.objects.create(
            product = obj,
            amount = obj.price,
            user = self.request.user
        )
        return redirect('pay', pk=order.pk)


class PayView(LoginRequiredMixin, DetailView):
    queryset = Order.objects.all()
    template_name = 'pay.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
