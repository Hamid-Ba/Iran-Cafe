"""
Zarinpal Module Serializers
"""
from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """Payment Serializer"""

    class Meta:
        """Meta Class"""

        model = Payment
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        cafe = self.context["request"].user.cafe

        if rep["cafe"] == cafe:
            return rep
        return rep
