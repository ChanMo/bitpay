from django.urls import path
from .views import CheckoutView, PayView

urlpatterns = [
    path('<int:pk>/checkout/', CheckoutView.as_view(), name='checkout'),
    path('<int:pk>/pay/', PayView.as_view(), name='pay'),
]
