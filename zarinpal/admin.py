from jalali_date.admin import ModelAdminJalaliMixin

from django.contrib import admin
from .models import Payment, StorePayment


class PaymentAdmin(ModelAdminJalaliMixin,admin.ModelAdmin):
    """Payment admin"""

    list_display = [
        "cafe",
        "plan",
        "pay_amount",
        "ref_id",
        "is_payed",
        "status",
        "payed_date",
        "created_date",
    ]
    list_display_links = ["cafe", "plan", "pay_amount", "created_date"]
    ordering = ["id"]
    list_editable = ("payed_date",)
    search_fields = ["plan__title", "cafe__code"]

    @admin.display(ordering="plan__title")
    def cafe_code(self, obj):
        return obj.plan.title


class StorePaymentAdmin(ModelAdminJalaliMixin,admin.ModelAdmin):
    """Store Payment admin"""

    list_display = [
        "cafe",
        "user",
        "order",
        "pay_amount",
        "ref_id",
        "is_payed",
        "status",
        "payed_date",
        "created_date",
    ]
    list_display_links = ["cafe", "user", "order", "pay_amount", "created_date"]
    ordering = ["id"]
    list_editable = ("payed_date",)
    
    search_fields = ["user__phone", "user__fullName", "cafe__code"]


admin.site.register(Payment, PaymentAdmin)
admin.site.register(StorePayment, StorePaymentAdmin)
