from uuid import uuid4
from rest_framework import serializers

from . import models


class SubCategorySerializer(serializers.ModelSerializer):
    """Category Serializer"""

    class Meta:
        model = models.StoreCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """Category Serializer"""

    sub_category = SubCategorySerializer(many=True)

    class Meta:
        model = models.StoreCategory
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    """Product Serializer"""

    category = CategorySerializer(read_only=True)

    class Meta:
        model = models.Product
        fields = "__all__"


class StoreOrderItemSerializer(serializers.ModelSerializer):
    """Order Item Serializer"""

    class Meta:
        model = models.StoreOrderItem
        fields = "__all__"
        read_only_fields = ("order",)


class StoreOrderSerializer(serializers.ModelSerializer):
    """Order Serializer"""

    items = StoreOrderItemSerializer(many=True)

    class Meta:
        model = models.StoreOrder
        fields = "__all__"
        read_only_fields = ("code", "state")

    def _add_items(self, order, items):
        for item in items:
            order.items.create(
                product_id=item["product_id"],
                title=item["title"],
                image_url=item["image_url"],
                desc=item["desc"],
                price=item["price"],
                count=item["count"],
            )

            product_item = models.Product.objects.filter(id=item["product_id"])
            if product_item.exists():
                product_item.first().ordered(item["count"])

    def create(self, validated_data):
        """Custom Create"""
        items = validated_data.pop("items", [])
        code = str(uuid4())[:5]

        order = models.StoreOrder.objects.create(code=code, **validated_data)
        self._add_items(order, items)
        order.save()

        return order
