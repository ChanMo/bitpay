from rest_framework.viewsets import ModelViewSet
from .serializers import OrderSerializer
from .models import Order


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
