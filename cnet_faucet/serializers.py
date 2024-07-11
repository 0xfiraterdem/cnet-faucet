from rest_framework import serializers
from .models import FaucetRequest


class FaucetRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaucetRequest
        fields = ['wallet_address', 'request_time']
