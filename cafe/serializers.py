"""
Cafe Module Serializers
"""
from django_jalali.serializers.serializerfield import JDateField, JDateTimeField
from uuid import uuid4
from rest_framework import serializers
from cafe.models import Cafe, Category, Gallery, MenuItem, Order, OrderItem, Reservation, Suggestion
from province.serializers import CitySerializer, ProvinceSerializer

class CreateUpdateCafeSerializer(serializers.ModelSerializer):
    """Cafe Serializer For Register Cafe"""
    class Meta:
        """Meta Class"""
        model = Cafe
        fields = ['persian_title', 'english_title' , 'phone' , 'street',
                    'desc' , 'type' , 'province' , 'city']

    def create(self, validated_data):
        """Register Cafe"""
        province = validated_data.pop('province' , None)
        city = validated_data.pop('city' , None)
        
        cafe = Cafe.objects.create(province=province,city=city,**validated_data)

        return cafe

class CafeSerializer(CreateUpdateCafeSerializer):
    """Cafe Serializer"""
    province = ProvinceSerializer()
    city = CitySerializer()
    class Meta(CreateUpdateCafeSerializer.Meta):
        """Meta Class"""
        # fields = ['id'] + CreateUpdateCafeSerializer.Meta.fields + ['image_url', 'instagram_id' , 'telegram_id' ,
        #                                             'postal_code', 'code', 'state' , 'owner' , 'view_count'] 
        fields = '__all__'
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


class CreateUpdateGallerySerializer(serializers.ModelSerializer):
    """Create or Update Gallery Serializer"""
    class Meta:
        """Meta Class"""
        model = Gallery
        fields = ['id','title','image']
        read_only_fields = ['id']

class GallerySerializer(CreateUpdateGallerySerializer):
    """Gallery Serializer"""
    class Meta(CreateUpdateGallerySerializer.Meta):
        """Meta Class"""
        fields = "__all__"

class SuggestionSerializer(serializers.ModelSerializer):
    """Suggestion Serializer"""
    class Meta:
        """Meta Class"""
        model = Suggestion
        fields = "__all__"
        read_only_fields = ['id']

    def create(self,validated_data):
        """Custom Create"""
        cafe = validated_data.pop('cafe',None)

        # cafe = Cafe.objects.filter(id=cafe_id).first()

        if cafe.state != 'C' :
            msg = 'کافه نامعتبر است'
            raise serializers.ValidationError(msg,code='Bad Request')
        
        suggest = Suggestion.objects.create(cafe=cafe,**validated_data)
        # suggest.save()

        return suggest

class CreateReservationSerializer(serializers.ModelSerializer):
    """Create Reservation Serializer"""
    class Meta:
        """Meta Class"""
        model = Reservation
        fields = ['id','cafe','full_name','phone','date','time','message']
        read_only_fields = ['id']

class PatchReservationSerializer(serializers.ModelSerializer):
    """Patch Reservation Serializer"""
    class Meta:
        """Meta Class"""
        model = Reservation
        fields = ['id','state']
        read_only_fields = ['id']

class ReservationSerializer(CreateReservationSerializer):
    """Reservation Serializer"""
    date = JDateField()
    class Meta(CreateReservationSerializer.Meta):
        """Meta Class"""
        fields = CreateReservationSerializer.Meta.fields + ['user','state']

class OrderItemSerializer(serializers.ModelSerializer):
    """Create Order Item Serializer"""
    class Meta:
        """Meta Class"""
        model = OrderItem
        fields = '__all__'
        read_only_fields = ['id','order']

class CreateOrderSerializer(serializers.ModelSerializer):
    """Create Order Serializer"""
    items = OrderItemSerializer(many=True,required=True)
    class Meta:
        """Meta Class"""
        model = Order
        fields = ['total_price','cafe','items']

    def _add_items(self, order,items):
        for item in items:
            order.items.create(
                menu_item_id=item['menu_item_id'],
                title=item['title'],
                image_url=item['image_url'],
                desc =item['desc'],
                price=item['price'],
                count=item['count']
                )

    def create(self, validated_data):
        """Custom Create"""
        cafe = validated_data.pop('cafe', None)
        items = validated_data.pop('items', [])
        code = str(uuid4())[:5]

        order = Order.objects.create(cafe=cafe,code=code,**validated_data)
        self._add_items(order,items)
        order.save()
        
        return order

class CafeOrderSerializer(serializers.ModelSerializer):
    """Cafe Order Serializer"""
    class Meta:
        model = Cafe
        fields = ['id','code','persian_title']

class OrderSerializer(CreateOrderSerializer,serializers.ModelSerializer):
    """Order Serializer"""
    cafe = CafeOrderSerializer()
    items = OrderItemSerializer(many=True)
    is_owner = serializers.SerializerMethodField()
    registered_date = JDateTimeField()

    def get_is_owner(self,obj):
        request = self.context.get('request', None)
        return Cafe.objects.filter(owner=request.user).exists()

    class Meta(CreateOrderSerializer.Meta):
        """Meta Class"""
        fields = ['id','code','state', 'registered_date','is_owner'] + CreateOrderSerializer.Meta.fields

class PatchOrderSerializer(serializers.ModelSerializer):
    """Patch Order Serializer"""
    class Meta:
        """Meta Class"""
        model = Order
        fields = ['id','state']