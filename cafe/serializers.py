"""
Cafe Module Serializers
"""
import json
from django_jalali.serializers.serializerfield import JDateField, JDateTimeField
from uuid import uuid4
from rest_framework import serializers
from django.contrib.auth import get_user_model
from random import randint
from websocket import create_connection
from django.conf import settings

from siteinfo.models import Error
from cafe.models import (
    Bartender,
    Cafe,
    Category,
    Customer,
    Gallery,
    MenuItem,
    Order,
    OrderItem,
    Reservation,
    Suggestion,
    Event,
    Branch,
    Table,
)
from province.serializers import CitySerializer, ProvinceSerializer
from notifications import KavenegarSMS
from cafe import tasks


class CreateCafeSerializer(serializers.ModelSerializer):
    """Cafe Serializer For Register Cafe"""

    class Meta:
        """Meta Class"""

        model = Cafe
        fields = [
            "persian_title",
            "english_title",
            "phone",
            "street",
            "desc",
            "type",
            "province",
            "city",
        ]

    def create(self, validated_data):
        """Register Cafe"""
        province = validated_data.pop("province", None)
        city = validated_data.pop("city", None)

        cafe = Cafe.objects.create(province=province, city=city, **validated_data)

        # Send SMS
        try:
            kavenegar = KavenegarSMS()
            kavenegar.register(cafe.phone)
            kavenegar.send()
        except Exception as e:
            Error.objects.create(
                reference="Cafe - serializers.py - kavenegar",
                status=str(type(e).__name__),
                description=str(e),
            )
            tasks.inform_manager_when_cafe_has_problem_to_receiving_sms.delay(cafe.id)
            tasks.inf

        tasks.inform_manager_when_cafe_registered.delay(cafe.id)

        return cafe


class UpdateCafeSerializer(CreateCafeSerializer):
    """Cafe Serializer"""

    class Meta(CreateCafeSerializer.Meta):
        """Meta Class"""

        fields = "__all__"
        read_only_fields = [
            "owner",
            "code",
            "state",
            "view_count",
            "charge_expired_date",
        ]


class CafeSerializer(CreateCafeSerializer):
    """Cafe Serializer"""

    province = ProvinceSerializer()
    city = CitySerializer()

    class Meta(CreateCafeSerializer.Meta):
        """Meta Class"""

        # fields = ['id'] + CreateUpdateCafeSerializer.Meta.fields + ['image_url', 'instagram_id' , 'telegram_id' ,
        #                                             'postal_code', 'code', 'state' , 'owner' , 'view_count']
        fields = "__all__"
        read_only_fields = [
            "owner",
            "code",
            "state",
            "view_count",
            "charge_expired_date",
        ]


class UserCafeSerializer(CafeSerializer):
    """User Cafe Serializer"""

    class Meta(CafeSerializer.Meta):
        """Meta Class"""

        fields = ["id", "state"]
        read_only_fields = ["id", "state"]


class CateogrySerializer(serializers.ModelSerializer):
    """Cateogry Serializer"""

    class Meta:
        """Meta Class"""

        model = Category
        fields = "__all__"
        read_only_fields = ["id", "cafe"]


class CreateUpdateMenuItemSerializer(serializers.ModelSerializer):
    """Cafe Serializer For Register Cafe"""

    class Meta:
        """Meta Class"""

        model = MenuItem
        fields = [
            "title",
            "image_url",
            "price",
            "desc",
            "is_active",
            "calorie",
            "category",
            "sort_index",
        ]

    def create(self, validated_data):
        """Create Menu Item"""
        category = validated_data.pop("category", None)

        menuItem = MenuItem.objects.create(category=category, **validated_data)

        return menuItem


class MenuItemSerializer(CreateUpdateMenuItemSerializer):
    """Menu Item Serializer"""

    category = CateogrySerializer(required=True)

    class Meta(CreateUpdateMenuItemSerializer.Meta):
        """Meta Class"""

        fields = ["id"] + CreateUpdateMenuItemSerializer.Meta.fields


class CreateUpdateGallerySerializer(serializers.ModelSerializer):
    """Create or Update Gallery Serializer"""

    class Meta:
        """Meta Class"""

        model = Gallery
        fields = ["id", "title", "image"]
        read_only_fields = ["id"]


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
        read_only_fields = ["id"]

    def create(self, validated_data):
        """Custom Create"""
        cafe = validated_data.pop("cafe", None)

        if cafe.state != "C":
            msg = "کافه نامعتبر است"
            raise serializers.ValidationError(msg, code="Bad Request")

        suggest = Suggestion.objects.create(cafe=cafe, **validated_data)
        return suggest


class CreateReservationSerializer(serializers.ModelSerializer):
    """Create Reservation Serializer"""

    class Meta:
        """Meta Class"""

        model = Reservation
        fields = ["id", "cafe", "full_name", "phone", "date", "time", "message"]
        read_only_fields = ["id"]


class PatchReservationSerializer(serializers.ModelSerializer):
    """Patch Reservation Serializer"""

    class Meta:
        """Meta Class"""

        model = Reservation
        fields = ["id", "state"]
        read_only_fields = ["id"]


class ReservationSerializer(CreateReservationSerializer):
    """Reservation Serializer"""

    date = JDateField()
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context.get("request", None)
        if Cafe.objects.filter(owner=request.user).exists():
            return "O"
        elif Bartender.objects.filter(user=request.user).exists():
            return "B"
        else:
            return "U"

    class Meta(CreateReservationSerializer.Meta):
        """Meta Class"""

        fields = CreateReservationSerializer.Meta.fields + ["user", "state", "is_owner"]


class OrderItemSerializer(serializers.ModelSerializer):
    """Create Order Item Serializer"""

    class Meta:
        """Meta Class"""

        model = OrderItem
        fields = "__all__"
        read_only_fields = ["id", "order"]


class CreateOrderSerializer(serializers.ModelSerializer):
    """Create Order Serializer"""

    items = OrderItemSerializer(many=True, required=True)

    class Meta:
        """Meta Class"""

        model = Order
        fields = ["total_price", "cafe", "items", "desc", "phone", "num_of_table"]

    def _add_items(self, order, items):
        for item in items:
            order.items.create(
                menu_item_id=item["menu_item_id"],
                title=item["title"],
                image_url=item["image_url"],
                desc=item["desc"],
                price=item["price"],
                count=item["count"],
            )

            menu_item = MenuItem.objects.filter(id=item["menu_item_id"])
            if menu_item.exists():
                menu_item.first().ordered(item["count"])

    def create(self, validated_data):
        """Custom Create"""
        cafe = validated_data.pop("cafe", None)
        items = validated_data.pop("items", [])
        code = str(uuid4())[:5]

        order = Order.objects.create(cafe=cafe, code=code, **validated_data)
        self._add_items(order, items)
        order.save()

        # Notify WebSocket consumers about the new order
        try:
            self._send_order_notification(order, cafe)
        except Exception as e:
            print("We Are In Test Mode")
            
        return order

    def _send_order_notification(self, order, cafe):
        """Send A message to order WS"""    
        url = "ws://127.0.0.1:8000/ws/order/"  
        if not settings.DEBUG:
            url = "ws://127.0.0.1:8001/ws/order/"
            
        ws = create_connection(url)
        ws.send(json.dumps({"order":f"{order.id}", "cafe":f"{cafe.id}", "message":"سفارش جدیدی اضافه شد"}))
        result =  ws.recv()
        print (result)
        ws.close()


class CafeOrderSerializer(serializers.ModelSerializer):
    """Cafe Order Serializer"""

    class Meta:
        model = Cafe
        fields = ["id", "code", "persian_title"]


class OrderSerializer(CreateOrderSerializer, serializers.ModelSerializer):
    """Order Serializer"""

    cafe = CafeOrderSerializer()
    items = OrderItemSerializer(many=True)
    is_owner = serializers.SerializerMethodField()
    registered_date = JDateTimeField()

    def get_is_owner(self, obj):
        request = self.context.get("request", None)
        if Cafe.objects.filter(owner=request.user).exists():
            return "O"
        elif Bartender.objects.filter(user=request.user).exists():
            return "B"
        else:
            return "U"

    class Meta(CreateOrderSerializer.Meta):
        """Meta Class"""

        fields = [
            "id",
            "code",
            "state",
            "registered_date",
            "is_owner",
        ] + CreateOrderSerializer.Meta.fields


class PatchOrderSerializer(serializers.ModelSerializer):
    """Patch Order Serializer"""

    class Meta:
        """Meta Class"""

        model = Order
        fields = ["id", "state"]


class CreateBartenderSerializer(serializers.Serializer):
    """Create Bartneder Serializer"""

    phone = serializers.CharField(
        max_length=11,
        required=True,
        error_messages={
            "blank": "موبایل خود را وارد نمایید",
            "required": "موبایل خود را وارد نمایید",
        },
    )

    def validate(self, attrs):
        phone = attrs.get("phone")

        if not phone.isdigit():
            return super().validate(attrs)

        return attrs

    def create(self, validated_data):
        phone = validated_data.get("phone", None)
        otp = str(randint(100000, 999999))

        owner = self.context.get("request").user
        # if owner.cafe == None:
        #     msg = 'اول کافه خود را ثبت نمایید'
        #     raise serializers.ValidationError(msg)

        if Cafe.objects.filter(owner__phone=phone).exists():
            msg = "این کاربر ، کافه دار است"
            raise serializers.ValidationError(msg)

        if Bartender.objects.filter(user__phone=phone).exists():
            msg = "شما قادر به ثبت این بارتندر نمی باشید"
            raise serializers.ValidationError(msg)

        user, created = get_user_model().objects.get_or_create(phone=phone)
        user.set_password(otp)
        user.save()

        bartender = Bartender.objects.create(user=user, cafe=owner.cafe)

        return bartender


class BartnederSerializer(serializers.ModelSerializer):
    """Bartneder Serializer"""

    class Meta:
        """Meta Class"""

        model = Bartender
        fields = "__all__"
        read_only_fields = ["id", "user", "cafe"]

    def create(self, validated_data):
        phone = validated_data.get("phone", None)
        otp = str(randint(100000, 999999))

        owner = self.context.get("request").user

        if owner.cafe == None:
            msg = "اول کافه خود را ثبت نمایید"
            raise serializers.ValidationError(msg)

        if Cafe.objects.filter(owner__phone=phone).exists():
            msg = "این کاربر ، کافه دار است"
            raise serializers.ValidationError(msg)

        if Bartender.objects.filter(user__phone=phone).exists():
            msg = "شما قادر به ثبت این بارتندر نمی باشید"
            raise serializers.ValidationError(msg)

        user, created = get_user_model().objects.get_or_create(phone=phone)

        if user.is_staff or user.is_superuser:
            msg = "شما قادر به ثبت این کاربر نمی باشید"
            raise serializers.ValidationError(msg)

        user.set_password(otp)
        user.save()

        bartender = Bartender.objects.create(phone=phone, user=user, cafe=owner.cafe)
        bartender.save()

        return bartender

    def update(self, instance, validated_data):
        phone = validated_data.get("phone", None)
        old_phone = instance.phone

        if phone:
            if get_user_model().objects.filter(phone=phone).exists():
                msg = "همچین کاربری وجود دارد"
                raise serializers.ValidationError(msg)

            if Cafe.objects.filter(owner__phone=phone).exists():
                msg = "این کاربر ، کافه دار است"
                raise serializers.ValidationError(msg)

            if Bartender.objects.filter(user__phone=phone).exists():
                msg = "شما قادر به ثبت این بارتندر نمی باشید"
                raise serializers.ValidationError(msg)

            bartender = Bartender.objects.get(phone=old_phone)
            bartender.phone = phone

            user = get_user_model().objects.get(phone=old_phone)
            user.phone = phone
            user.save()

        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.save()
        return instance

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["phone"] = instance.user.phone
        return response


class CustomerSerializer(serializers.ModelSerializer):
    """Customer Serializer"""

    class Meta:
        model = Customer
        fields = "__all__"
        read_only_fields = ["id", "user", "phone"]

    def create(self, validated_data):
        cafe = validated_data.pop("cafe", None)
        user = self.context["request"].user

        customer = Customer.objects.create(
            user=user, cafe=cafe, phone=user.phone, **validated_data
        )
        customer.save()

        return customer

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["cafe"] = instance.cafe.persian_title
        response["cafe_id"] = instance.cafe.id
        response["cafe_code"] = instance.cafe.code

        return response


class EventSerializer(serializers.ModelSerializer):
    """Event Serializer"""

    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = ["id", "cafe", "created_date", "is_expired"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep["cafe"] = {
            "id": instance.cafe.id,
            "code": instance.cafe.code,
            "persian_title": instance.cafe.persian_title,
            "english_title": instance.cafe.english_title,
        }
        return rep


class CafeEventsSerializer(serializers.ModelSerializer):
    """Cafe Events Serializer"""

    events = EventSerializer(many=True)

    class Meta:
        model = Cafe
        fields = ["id", "persian_title", "english_title", "code", "events"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep.clear()

        rep["cafe"] = {
            "id": instance.id,
            "code": instance.code,
            "persian_title": instance.persian_title,
            "english_title": instance.english_title,
        }

        rep["events"] = (
            instance.events.filter(status=True, is_expired=False)
            .order_by("-created_date")
            .values()
        )

        return rep


class BranchSerializer(serializers.ModelSerializer):
    """Branch Serializer"""

    class Meta:
        model = Branch
        fields = "__all__"
        read_only_fields = ["cafe"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep["province"] = {"id": instance.province.id, "name": instance.province.name}

        rep["city"] = {"id": instance.city.id, "name": instance.city.name}

        return rep


class CafeBranchesSerializer(serializers.ModelSerializer):
    """Cafe Branches Serializer"""

    branches = BranchSerializer(many=True)

    class Meta:
        model = Cafe
        fields = ["id", "persian_title", "english_title", "code", "branches"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep.clear()

        rep["cafe"] = {
            "id": instance.id,
            "code": instance.code,
            "persian_title": instance.persian_title,
            "english_title": instance.english_title,
        }

        rep["branches"] = (
            instance.branches.filter(is_active=True).order_by("-id").values()
        )

        return rep


class TableSerializer(serializers.ModelSerializer):
    """Table Serializer"""

    cafe = CafeSerializer(many=False, read_only=True)

    class Meta:
        model = Table
        fields = ["id", "number", "qr_code", "cafe"]
        read_only_fields = ["id", "number", "qr_code", "cafe"]

    # def validate(self, attrs):
    #     cafe = attrs.get("cafe")
    #     number = attrs.get("number")

    #     if Table.objects.filter(cafe=cafe, number=number).exists():
    #         msg = "شما این میز را قبلا تعریف کرده اید"
    #         raise serializers.ValidationError(msg)

    #     return attrs

    def create(self, validated_data):
        cafe = validated_data.pop("cafe", None)

        number = cafe.tables_count() + 1

        qr_code_data = f"https://cafesiran.ir/cafes/{cafe.id}?table={number}"
        qr_code = f"https://api.qrserver.com/v1/create-qr-code/?data={qr_code_data}&size=200x200"

        table = Table.objects.create(cafe=cafe, number=number, qr_code=qr_code)
        table.save()

        return table

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["cafe"] = {"id": rep["cafe"].get("id"), "code": rep["cafe"].get("code")}
        return rep
