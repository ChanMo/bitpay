from rest_framework import serializers
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        # exclude = ('private_key',)
        fields = '__all__'
        
