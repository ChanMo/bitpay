from django.views.generic import ListView
from .models import Product


class IndexView(ListView):
    queryset = Product.objects.all()
    template_name = 'index.html'
