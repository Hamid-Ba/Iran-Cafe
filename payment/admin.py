from django.contrib import admin
from .models import Payment


class PaymentAdmin(admin.ModelAdmin):
    """Customer admin"""

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

    search_fields = ["plan__title", "cafe__code"]

    @admin.display(ordering="cafe__code")
    def cafe_code(self, obj):
        return obj.cafe.code

    @admin.display(ordering="plan__title")
    def cafe_code(self, obj):
        return obj.plan.title


admin.site.register(Payment, PaymentAdmin)
