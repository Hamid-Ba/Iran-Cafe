"""
Province Module Serializers
"""
from rest_framework import serializers
from django.contrib.auth import (get_user_model)

from province.models import (Province , City)

class ProvinceSerializer(serializers.ModelSerializer):
    """Province Serializer"""
    class Meta:
        """Meta Class"""
        model = Province
        fields = ['id']

class CitySerializer(serializers.ModelSerializer):
    """City Serializer"""
    class Meta:
        """City Serializer"""
        model = City
        fields = ['id']