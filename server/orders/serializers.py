from rest_framework import serializers
from accounts.models import get_free_account
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('account', 'status', 'expired_at')

    def create(self, validated_data):
        return Order.objects.create(
            **validated_data,
            account = get_free_account()
        )
