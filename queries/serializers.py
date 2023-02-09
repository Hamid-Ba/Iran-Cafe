from rest_framework import serializers

from cafe.models import OrderItem


class OrderItemQuerySerializer(serializers.ModelSerializer):
    """Order Query Serializer"""

    class Meta:
        """Meta Class"""

        model = OrderItem
        fields = "__all__"


class OrderQuerySerializer(serializers.Serializer):
    """Order Query Serializer"""

    items = OrderItemQuerySerializer(many=True)
    # total_price = serializers.DecimalField(max_digits=10,decimal_places=0)
