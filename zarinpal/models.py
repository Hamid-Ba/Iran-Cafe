"""
Payment Models Module
"""
from django.db import models
from djmoney.models.fields import MoneyField

from cafe import models as cafe_models
from plan import models as plan_models


class Payment(models.Model):
    """Payment Model"""

    class PaymentStatus(models.IntegerChoices):
        """Payment Status Enums"""

        PAYMENT_CREATED = 1, "Payment Created"
        PAYMENT_DONE = 2, "Payment Done"
        PAYMENT_CANCELLED = 3, "Payment Cancelled"

    pay_amount = MoneyField(
        max_digits=10, decimal_places=0, default_currency="IRR", null=False
    )
    desc = models.CharField(max_length=125, null=True, blank=True)
    ref_id = models.CharField(max_length=50, null=True, blank=True)
    authority = models.CharField(max_length=50, null=True, blank=True)
    is_payed = models.BooleanField(default=False)
    payed_date = models.DateTimeField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.PositiveSmallIntegerField(
        choices=PaymentStatus.choices, default=PaymentStatus.PAYMENT_CREATED
    )

    cafe = models.ForeignKey(
        cafe_models.Cafe, on_delete=models.CASCADE, related_name="payments"
    )
    plan = models.ForeignKey(
        plan_models.Plan, on_delete=models.CASCADE, related_name="payments"
    )

    def __str__(self) -> str:
        return f"Cafe Code : {self.cafe.code} , Cafe Title : {self.cafe.persian_title}"