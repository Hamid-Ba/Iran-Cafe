"""
Cafe Module Models
"""
import math
import os
import pytz
from uuid import uuid4
from django.db import models
from django.conf import settings
from datetime import datetime, timedelta

from djmoney.models.fields import MoneyField

from cafe.validators import phone_validator
from notifications import KavenegarSMS
from province.models import City, Province


class CafeManager(models.Manager):
    """Cafe Manager"""

    def get_confirmed_cafes(self):
        """Returns a list of cafes that have been confirmed"""
        return self.filter(state="C").values()

    def get_charged_and_confirmed_cafes(self):
        """Returns a list of cafes that have been charged and confirmed"""
        confirmed = self.get_confirmed_cafes()
        confirmed_and_charged = confirmed.filter(
            charge_expired_date__gte=datetime.now()
        ).values()
        return confirmed_and_charged

    def get_by_province(self, province):
        """Get By Province"""
        return (
            self.get_charged_and_confirmed_cafes()
            .filter(province__slug=province)
            .order_by("-view_count")
            .values()
        )

    def get_by_city(self, city):
        """Get By City"""
        return (
            self.get_charged_and_confirmed_cafes()
            .filter(city__slug=city)
            .order_by("-view_count")
            .values()
        )

    def fill_unique_code(self, cafe_id):
        """Change Cafe State to Confirmed"""
        cafe = self.filter(id=cafe_id).get()
        if cafe.state == "C":
            if not cafe.code:
                cafe.code = str(10000 + cafe_id)
                cafe.charge_cafe(days=31, is_first=True)
                cafe.save()

                # Send Confirm SMS
                kavenegar = KavenegarSMS()
                kavenegar.confirm(cafe.phone, cafe.code)
                kavenegar.send()

        return cafe

    def get_valid_cafe_by_id(self, cafe_id: int):
        """Return Cafe If Confirmed and Charged"""
        return self.filter(
            id=cafe_id, state="C", charge_expired_date__gte=datetime.now()
        ).first()

    def get_valid_cafe_by_code(self, cafe_code: str):
        """Return Cafe If Confirmed and Charged"""
        return self.filter(
            code=cafe_code, state="C", charge_expired_date__gte=datetime.now()
        ).first()

    def get_expired_cafes(self):
        """Return Expired Cafes"""
        return self.filter(state="C", charge_expired_date__lt=datetime.now()).all()


class Cafe(models.Model):
    """Cafe Model"""

    class CafeType(models.TextChoices):
        CAFE = "C", "CAFE"
        RESTAURANT = (
            "R",
            "RESTAURANT",
        )
        CAFE_RESTAURANT = (
            "CR",
            "CAFE_RESTAURANT",
        )
        ICE_CREAM = "IC", "ICE_CREAM_PARLOR"

    class CafeState(models.TextChoices):
        PENDING = "P", "Pending"
        CONFIRMED = "C", "Confirmed"
        REJECTED = "R", "Rejected"

    class CafeExpiredStatus(models.TextChoices):
        Informed = "I", "Informed"
        Need_To_Be_Informed = "N", "Need To Be Informed"
        Charged = "C", "Charged"

    code = models.CharField(max_length=5, unique=True, null=True, blank=True)
    persian_title = models.CharField(max_length=85, null=False, blank=False)
    english_title = models.CharField(max_length=90, null=False, blank=False)
    # slug = models.SlugField(max_length=200,unique=True,blank=False,null=False)
    phone = models.CharField(max_length=11, unique=True, validators=[phone_validator])
    email = models.EmailField(max_length=125, null=True, blank=True)
    image_url = models.URLField(
        max_length=250,
        blank=True,
        null=True,
        error_messages={"invalid": "مقدار وارد شده صحیح نم باشد"},
    )
    menu_url = models.URLField(
        max_length=250,
        blank=True,
        null=True,
        error_messages={"invalid": "مقدار وارد شده صحیح نم باشد"},
    )
    telegram_id = models.CharField(max_length=100, blank=True, null=True)
    instagram_id = models.CharField(max_length=100, blank=True, null=True)
    google_map_url = models.URLField(
        max_length=250,
        blank=True,
        null=True,
        error_messages={"invalid": "مقدار وارد شده صحیح نم باشد"},
    )
    street = models.CharField(max_length=250, null=True, blank=True)
    desc = models.TextField(blank=True, null=True)
    state = models.CharField(
        max_length=1, default=CafeState.PENDING, choices=CafeState.choices
    )
    type = models.CharField(
        max_length=2, default=CafeType.CAFE, choices=CafeType.choices
    )
    view_count = models.BigIntegerField(default=0)
    charge_expired_date = models.DateTimeField(null=True, blank=True)
    is_notify_expired_from_back = models.CharField(
        max_length=1,
        default=CafeExpiredStatus.Charged,
        choices=CafeExpiredStatus.choices,
    )
    is_notify_expired_from_front = models.CharField(
        max_length=1,
        default=CafeExpiredStatus.Charged,
        choices=CafeExpiredStatus.choices,
    )
    latitude = models.CharField(max_length=125, blank=True, null=True)
    longitude = models.CharField(max_length=125, blank=True, null=True)
    is_open = models.BooleanField(default=False)
    tax = models.SmallIntegerField(default=0)

    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cafe"
    )
    province = models.ForeignKey(Province, on_delete=models.DO_NOTHING)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)

    objects = CafeManager()

    def __str__(self) -> str:
        return self.persian_title

    def add_view(self):
        self.view_count += 1
        self.save()

    def charge_cafe(self, days, is_first=False):
        """Charge Cafe Date By Given Days"""
        # First Free Charge
        utc = pytz.UTC

        if is_first and not self.charge_expired_date:
            self.charge_expired_date = datetime.now() + timedelta(days=days)
        # When Purchesd Plan
        elif not is_first:
            # When Date is expired
            charge_expired_date = self.charge_expired_date.replace(tzinfo=utc)
            now = datetime.now().replace(tzinfo=utc)

            if self.charge_expired_date and charge_expired_date < now:
                self.charge_expired_date = datetime.now() + timedelta(days=days)
            # When has charge but want to charge
            else:
                self.charge_expired_date += timedelta(days=days)

            self.is_notify_expired_from_back = self.CafeExpiredStatus.Charged
        self.save()

    def set_notified_expired(self, is_back=True, value="I"):
        if is_back:
            self.is_notify_expired_from_back = value
        else:
            self.is_notify_expired_from_front = value
        self.save()

    def tables_count(self):
        """Return Cafe Tables Count"""
        return self.tables.count()

    def last_table(self):
        """Rerturn Last Table"""
        try:
            return self.tables.order_by("-number").first()
        except:
            return None


class Table(models.Model):
    """Table Model"""

    number = models.PositiveIntegerField(blank=False, null=False)
    qr_code = models.URLField(
        max_length=250,
        blank=True,
        null=True,
    )

    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name="tables")

    def __str__(self) -> str:
        return f"Table : {self.number} - Cafe : {self.cafe.code}"

    class Meta:
        unique_together = (
            "number",
            "cafe",
        )


class Branch(models.Model):
    """Branch model"""

    latitude = models.CharField(max_length=125, blank=True, null=True)
    longitude = models.CharField(max_length=125, blank=True, null=True)
    street = models.CharField(max_length=250, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name="branches")
    province = models.ForeignKey(
        Province, on_delete=models.DO_NOTHING, related_name="branches"
    )
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING, related_name="branches")

    def __str__(self) -> str:
        return f"{self.cafe.code}-{self.province}-{self.city}-{self.street}"


def category_image_file_path(instance, filename):
    """Generate file path for category image"""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid4()}.{ext}"

    return os.path.join("uploads", "category", filename)


class Category(models.Model):
    """Category model"""

    order = models.IntegerField(null=True, blank=True, default=1)
    title = models.CharField(max_length=72, null=False, blank=False)
    image = models.ImageField(null=True, blank=True, upload_to=category_image_file_path)

    cafe = models.ForeignKey(
        Cafe, null=True, blank=True, on_delete=models.CASCADE, related_name="categories"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"


class MenuItemManager(models.Manager):
    """Menu Item Manager"""

    def get_active_items(self, cafe_id):
        return (
            self.filter(cafe__id=cafe_id)
            .filter(is_active=True)
            .order_by("sort_index")
            .values()
        )

    def get_list_by(self, cafe, category):
        return self.filter(cafe__id=cafe.id).filter(category__id=category.id)


class MenuItem(models.Model):
    """Menu Item model"""

    title = models.CharField(max_length=125, null=False, blank=False)
    image_url = models.URLField(
        max_length=250,
        blank=True,
        null=True,
        error_messages={"invalid": "مقدار وارد شده صحیح نم باشد"},
    )
    desc = models.TextField(null=False, blank=False)
    price = MoneyField(
        max_digits=10, decimal_places=0, default_currency="IRR", null=False
    )
    is_active = models.BooleanField(default=True)
    calorie = models.FloatField(null=True, blank=True)
    order_count = models.IntegerField(default=0)
    sort_index = models.PositiveIntegerField(null=True, blank=True, default=1)
    is_board_game = models.BooleanField(default=False)

    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name="menu_items")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="menu_items"
    )

    objects = MenuItemManager()

    def __str__(self):
        return self.title

    def ordered(self, count):
        self.order_count += count
        self.save()


def gallery_image_file_path(instance, filename):
    """Generate file path for category image"""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid4()}.{ext}"

    return os.path.join("uploads", "gallery", filename)


class Gallery(models.Model):
    """Gallery model"""

    title = models.CharField(max_length=125, blank=True, null=True)
    image = models.ImageField(null=False, upload_to=gallery_image_file_path)

    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name="gallery")

    def __str__(self):
        if self.title:
            return self.title
        return self.image

    class Meta:
        verbose_name_plural = "Galleries"


class Suggestion(models.Model):
    """Suggestions model"""

    full_name = models.CharField(max_length=125, blank=True, null=True)
    message = models.TextField(blank=False, null=False)

    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name="suggest")

    def __str__(self):
        return self.cafe.code


class ReservationManager(models.Manager):
    """Reservation Manager"""

    def _get_cafe_reservation(self, cafe):
        return self.filter(cafe=cafe).order_by("-id")

    def _get_user_reservation(self, user):
        return self.filter(user=user).order_by("-id")

    def get_reservation(self, cafe, user, bartender=None):
        if cafe:
            return self._get_cafe_reservation(cafe)
        elif user:
            return self._get_user_reservation(user)
        elif bartender:
            cafe_reserves = self._get_cafe_reservation(bartender.cafe)
            user_reserves = self._get_user_reservation(bartender.user)
            return cafe_reserves | user_reserves

        return None


class Reservation(models.Model):
    """Reservation model"""

    class ReservationState(models.TextChoices):
        PENDING = "P", "Pending"
        CONFIRMED = "C", "Confirmed"
        REJECTED = "R", "Rejected"

    full_name = models.CharField(max_length=125, blank=False, null=False)
    phone = models.CharField(max_length=11, validators=[phone_validator])
    date = models.DateField(blank=False, null=False)
    time = models.TimeField(blank=False, null=False)
    message = models.CharField(max_length=500, blank=True, null=True)
    state = models.CharField(
        max_length=1, default=ReservationState.PENDING, choices=ReservationState.choices
    )

    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name="reserve")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reserve"
    )

    objects = ReservationManager()


class OrderManager(models.Manager):
    """Order Manager"""

    def _get_cafe_order(self, cafe):
        return self.filter(cafe=cafe).order_by("-registered_date")

    def _get_user_order(self, user):
        return self.filter(user=user).order_by("-registered_date")

    def get_order(self, state, code, cafe, user, bartender=None):
        if cafe:
            orders = self._get_cafe_order(cafe)
            if state != "all" or not state:
                orders = orders.filter(state=state)
            return orders.filter(code__contains=code)
        elif user:
            orders = self._get_user_order(user)
            if state != "all" or not state:
                orders = orders.filter(state=state)
            return orders.filter(code__contains=code)
        elif bartender:
            cafe_orders = self._get_cafe_order(bartender.cafe)
            user_orders = self._get_user_order(bartender.user)
            orders = cafe_orders | user_orders
            if state != "all" or not state:
                orders = orders.filter(state=state)
            return orders.filter(code__contains=code)

        return None


class Order(models.Model):
    """Order model"""

    class OrderState(models.TextChoices):
        PENDING = "P", "Pending"
        CONFIRMED = "D", "Delivered"
        REJECTED = "C", "Cancelled"

    code = models.CharField(max_length=5, blank=False, null=True)
    state = models.CharField(
        max_length=1, default=OrderState.PENDING, choices=OrderState.choices
    )
    total_price = MoneyField(
        max_digits=10, decimal_places=0, default_currency="IRR", null=False
    )
    registered_date = models.DateTimeField(auto_now_add=True, editable=False)
    delivered_date = models.DateTimeField(
        auto_now_add=False, editable=True, null=True, blank=True
    )
    phone = models.CharField(
        max_length=11,
        blank=False,
        null=False,
        validators=[phone_validator],
        default="09151498722",
    )
    desc = models.CharField(max_length=500, blank=True, null=True)
    num_of_table = models.IntegerField(default=0)

    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name="order")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="order"
    )

    objects = OrderManager()

    def __str__(self):
        return self.user.phone
    
    def delivered(self):
        self.state = Order.OrderState.CONFIRMED
        self.delivered_date = datetime.now()
        self.save()

    def calc_total_price(self, delivered_date):
        total_price = 0.0
        for item in self.items.all():
            item_price = 0
            if item.is_board_game:
                item_price = self._calc_board_game_price(
                    delivered_date, self.registered_date, item.price
                )

            else:
                item_price = item.price * item.count

            total_price += item_price

        self.total_price.amount = total_price
        self.save()

    def _calc_board_game_price(self, registered_date, delivered_date, price):
        """Claculate Board Game Price By Time Priod"""
        reg_time = registered_date.time()
        del_time = delivered_date.time()

        hour = (del_time.hour - reg_time.hour) * 3600
        minute = abs(del_time.minute - reg_time.minute) * 60
        second = abs(del_time.second - reg_time.second)

        different_time = (hour + minute + second) / 60

        if different_time < 1:
            different_time = 1

        return price * different_time


class OrderItem(models.Model):
    """OrderItem model"""

    # item = models.ForeignKey(MenuItem, on_delete=models.DO_NOTHING,related_name='items')
    menu_item_id = models.BigIntegerField(null=False, blank=False)
    title = models.CharField(max_length=125, null=False, blank=False)
    image_url = models.CharField(max_length=250, null=True, blank=True)
    desc = models.TextField(null=False, blank=False)
    price = MoneyField(
        max_digits=10, decimal_places=0, default_currency="IRR", null=False
    )
    count = models.IntegerField(default=0)
    is_board_game = models.BooleanField(default=False)

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")


class Bartender(models.Model):
    """Bartender model"""

    phone = models.CharField(max_length=11, unique=True, validators=[phone_validator])
    is_active = models.BooleanField(default=True)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bartender"
    )
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name="bartender")

    def __str__(self) -> str:
        return self.phone


class Customer(models.Model):
    """Customer model"""

    phone = models.CharField(
        max_length=11, null=False, blank=False, validators=[phone_validator]
    )
    firstName = models.CharField(max_length=65, blank=False, null=False)
    lastName = models.CharField(max_length=85, blank=False, null=False)
    birthdate = models.DateField(null=False, blank=False)

    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name="customers")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="customers"
    )

    def __str__(self) -> str:
        return f"{self.firstName} {self.lastName}"


class Event(models.Model):
    """Event model"""

    title = models.CharField(max_length=125)
    content = models.CharField(max_length=500)
    status = models.BooleanField(default=False)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_expired = models.BooleanField(default=False)

    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name="events")

    def __str__(self) -> str:
        return self.title
