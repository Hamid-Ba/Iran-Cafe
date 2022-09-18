"""
site info modules serializers
"""
from siteinfo.models import (AboutUs)

from rest_framework import serializers

class AboutUsSerializer(serializers.ModelSerializer):
    """About Us Serializer"""
    class Meta:
        """Meta Class"""
        model = AboutUs
        fields = '__all__'
        read_only_fields = ['id','phones','address','emails','text']