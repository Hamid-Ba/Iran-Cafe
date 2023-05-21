from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from djmoney.models.fields import MoneyField
from django.conf import settings

from cafe.models import Cafe
from config.validators import PhoneValidator

# Create your models here.


class StoreCategory(models.Model):
    title = models.CharField(max_length=255)
    sortitem = models.IntegerField(default=0)
    sub_category = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    price = MoneyField(
        max_digits=10, decimal_places=0, default_currency="IRR", null=False
    )
    image_url = models.URLField(null=True, blank=True)
    category = models.ForeignKey(
        StoreCategory, on_delete=models.CASCADE, related_name="products"
    )
    minimum_choice = models.IntegerField(default=1)
    adding_count = models.IntegerField(default=1)

    order_count = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def ordered(self, count):
        self.order_count += count
        self.save()


class StoreOrder(models.Model):
    class OrderState(models.TextChoices):
        PENDING = "P", "Pending"
        CONFIRMED = "D", "Delivered"
        REJECTED = "C", "Cancelled"

    fullName = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=5, blank=False, null=True)
    state = models.CharField(
        max_length=1, default=OrderState.PENDING, choices=OrderState.choices
    )
    total_price = MoneyField(
        max_digits=10, decimal_places=0, default_currency="IRR", null=False
    )
    phone = models.CharField(
        max_length=11, blank=False, null=False, validators=[PhoneValidator]
    )
    registered_date = models.DateTimeField(auto_now_add=True, editable=False)
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=11)
    # phone_number = models.CharField(max_length=20, validators=[PhoneValidator])
    cafe = models.ForeignKey(
        Cafe,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="store_orders",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="store_orders"
    )

    def __str__(self):
        return f"Store Order #{self.id}-{self.code}"


class StoreOrderItem(models.Model):
    product_id = models.BigIntegerField(null=False, blank=False)
    title = models.CharField(max_length=125, null=False, blank=False)
    image_url = models.CharField(max_length=250, null=False, blank=False)
    desc = models.TextField()
    price = MoneyField(
        max_digits=10, decimal_places=0, default_currency="IRR", null=False
    )
    count = models.IntegerField(validators=[MinValueValidator(1)])

    order = models.ForeignKey(
        StoreOrder, on_delete=models.CASCADE, related_name="items"
    )
