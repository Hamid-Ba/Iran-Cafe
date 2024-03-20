from rest_framework import serializers

from cloud import models


class CloudyCustomerSerializer(serializers.ModelSerializer):
    """Cloudy Customer Serializer"""

    class Meta:
        """Meta Class"""

        model = models.CloudyCustomer
        fields = "__all__"
        read_only_fields = [
            "id",
            "cafe",
            "is_called",
            "is_confirmed",
            "is_deployed",
            "is_cancelled",
            "called_date",
            "confirmed_date",
            "deployed_date",
            "cancelled_date",
            "created_date",
        ]

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res["fullName"] = instance.fullName
        return res
