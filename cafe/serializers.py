"""
Cafe Module Serializers
"""
from rest_framework import serializers
from cafe.models import Cafe

from province.serializers import (CitySerializer, ProvinceSerializer)

class CreateUpdateCafeSerializer(serializers.ModelSerializer):
    """Cafe Serializer For Register Cafe"""
    # province = ProvinceSerializer(required=True,many=False)
    # city = CitySerializer(required=True,many=False)
    class Meta:
        """Meta Class"""
        model = Cafe
        fields = ['persian_title', 'english_title', 'slug' , 'phone' , 'street', 'short_desc',
                    'desc' , 'type' , 'province' , 'city']

    def create(self, validated_data):
        """Register Cafe"""
        province = validated_data.pop('province' , None)
        city = validated_data.pop('city' , None)
        
        cafe = Cafe.objects.create(province=province,city=city,**validated_data)
        # cafe.province = province
        # cafe.city = city

        return cafe

class CafeSerializer(CreateUpdateCafeSerializer):
    """Cafe Serializer"""
    class Meta(CreateUpdateCafeSerializer.Meta):
        """Meta Class"""
        fields = ['id'] + CreateUpdateCafeSerializer.Meta.fields + ['image_url', 'instagram_id' , 'telegram_id' ,
                                                    'postal_code', 'code', 'state' , 'owner'] 
        read_only_fields = ['owner' , 'code' , 'state']