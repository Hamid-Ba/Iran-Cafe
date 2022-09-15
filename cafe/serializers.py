"""
Cafe Module Serializers
"""
from dataclasses import fields
from rest_framework import serializers
from cafe.models import Cafe, Category, Gallery, MenuItem

class CreateUpdateCafeSerializer(serializers.ModelSerializer):
    """Cafe Serializer For Register Cafe"""
    class Meta:
        """Meta Class"""
        model = Cafe
        fields = ['persian_title', 'english_title', 'slug' , 'phone' , 'street',
                    'desc' , 'type' , 'province' , 'city']

    def create(self, validated_data):
        """Register Cafe"""
        province = validated_data.pop('province' , None)
        city = validated_data.pop('city' , None)
        
        cafe = Cafe.objects.create(province=province,city=city,**validated_data)

        return cafe

class CafeSerializer(CreateUpdateCafeSerializer):
    """Cafe Serializer"""
    class Meta(CreateUpdateCafeSerializer.Meta):
        """Meta Class"""
        fields = ['id'] + CreateUpdateCafeSerializer.Meta.fields + ['image_url', 'instagram_id' , 'telegram_id' ,
                                                    'postal_code', 'code', 'state' , 'owner' , 'view_count'] 
        read_only_fields = ['owner' , 'code' , 'state' , 'view_count']

class UserCafeSerializer(CafeSerializer):
    """User Cafe Serializer"""
    class Meta(CafeSerializer.Meta):
        """Meta Class"""
        fields = ['id' , 'state']
        read_only_fields = ['id' , 'state']

class CateogrySerializer(serializers.ModelSerializer):
    """Cateogry Serializer"""
    class Meta:
        """Meta Class"""
        model = Category
        fields = '__all__'
        read_only_fields = ['id']

class CreateUpdateMenuItemSerializer(serializers.ModelSerializer):
    """Cafe Serializer For Register Cafe"""
    class Meta:
        """Meta Class"""
        model = MenuItem
        fields = ['title', 'image_url' , 'price' , 'desc','is_active' , 'category']
                    
    def create(self, validated_data):
        """Create Menu Item"""
        category = validated_data.pop('category', None)

        menuItem = MenuItem.objects.create(category=category,**validated_data)

        return menuItem

class MenuItemSerializer(CreateUpdateMenuItemSerializer):
    """Menu Item Serializer"""
    category = CateogrySerializer(required=True)
    class Meta(CreateUpdateMenuItemSerializer.Meta):
        """Meta Class"""
        fields = ['id'] + CreateUpdateMenuItemSerializer.Meta.fields

class GallerySerializer(serializers.ModelSerializer):
    """Gallery Serializer"""
    class Meta:
        """Meta Class"""
        model = Gallery
        fields = "__all__"