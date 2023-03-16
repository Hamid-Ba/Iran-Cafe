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


class StoreOrderSerializer(serializers.ModelSerializer):
    """Order Serializer"""

    items = StoreOrderItemSerializer(many=True)

    class Meta:
        model = models.StoreOrder
        fields = "__all__"
