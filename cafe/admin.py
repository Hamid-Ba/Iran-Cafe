from jalali_date.admin import ModelAdminJalaliMixin

from django.contrib import admin

from cafe.models import (
    Bartender,
    Cafe,
    Category,
    Gallery,
    MenuItem,
    Order,
    OrderItem,
    Reservation,
    Suggestion,
    Customer,
    Event,
    Branch,
    Table,
)


class CafeAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    """Cafe Admin Model"""

    list_display = [
        "code",
        "owner",
        "persian_title",
        "english_title",
        "charge_expired_date",
        "is_notify_expired_from_back",
        "is_notify_expired_from_front",
        "view_count",
        "state",
        "is_open",
        "type",
        "province",
        "city",
    ]
    list_display_links = ["code", "owner", "persian_title", "english_title"]
    list_editable = [
        "state",
        "charge_expired_date",
        "is_notify_expired_from_back",
        "is_notify_expired_from_front",
    ]
    list_filter = ["province", "state", "type", "charge_expired_date", "is_open"]
    sortable_by = ["state", "type", "view_count", "charge_expired_date", "is_open"]

    search_fields = ["code", "owner__fullName", "persian_title", "english_title"]

    fieldsets = (
        (
            "General Info",
            {
                "fields": (
                    "code",
                    "owner",
                    "persian_title",
                    "english_title",
                    "image_url",
                    "tax",
                ),
            },
        ),
        (
            "Status Info",
            {
                "classes": ("collapse",),
                "fields": (
                    "state",
                    "type",
                    "charge_expired_date",
                    "is_notify_expired_from_back",
                    "is_notify_expired_from_front",
                ),
            },
        ),
        (
            "Contact Info",
            {
                "classes": ("collapse",),
                "fields": ("phone", "email", "telegram_id", "instagram_id"),
            },
        ),
        (
            "Address Info",
            {
                "classes": ("collapse",),
                "fields": ("province", "city", "street", "google_map_url"),
            },
        ),
        (
            "Extra Info",
            {
                "classes": ("collapse",),
                "fields": (
                    "desc",
                    "menu_url",
                    "view_count",
                ),
            },
        ),
    )


class CategoryAdmin(admin.ModelAdmin):
    """Category Admin Model"""

    list_display = ["id", "title", "order", "cafe"]
    list_display_links = ["id", "title"]
    list_editable = ["cafe", "order"]
    sortable_by = ["title", "order", "cafe"]


class MenuItemAdmin(admin.ModelAdmin):
    """Menu Item Admin Model"""

    list_display = [
        "title",
        "price",
        "cafe",
        "cafe_code",
        "cafe_owner",
        "order_count",
        "is_active",
    ]
    list_display_links = ["title", "price"]
    list_editable = ["is_active"]
    list_filter = ["is_active", "cafe__code", "cafe__owner__phone"]
    sortable_by = ["title", "price"]
    search_fields = ["title", "cafe__code", "cafe__owner__phone"]

    @admin.display(ordering="cafe__code")
    def cafe_code(self, obj):
        return obj.cafe.code

    @admin.display(ordering="cafe__owner__phone")
    def cafe_owner(self, obj):
        return obj.cafe.owner.phone


class GalleryAdmin(admin.ModelAdmin):
    """Gallery Admin Model"""

    list_display = ["id", "title", "cafe", "cafe_code", "cafe_owner"]
    list_display_links = ["id", "title"]
    list_filter = ["cafe__code", "cafe__owner__phone"]
    sortable_by = ["title"]
    search_fields = ["title", "cafe__code", "cafe__owner__phone"]

    @admin.display(ordering="cafe__code")
    def cafe_code(self, obj):
        return obj.cafe.code

    @admin.display(ordering="cafe__owner__phone")
    def cafe_owner(self, obj):
        return obj.cafe.owner.phone


class SuggestionAdmin(admin.ModelAdmin):
    """Suggestion Admin Model"""

    list_display = ["id", "full_name", "cafe", "cafe_code", "cafe_owner"]
    list_display_links = ["id", "full_name"]
    list_filter = ["cafe__code", "cafe__owner__phone"]
    sortable_by = ["id", "full_name"]
    search_fields = ["full_name", "cafe__code", "cafe__owner__phone"]

    @admin.display(ordering="cafe__code")
    def cafe_code(self, obj):
        return obj.cafe.code

    @admin.display(ordering="cafe__owner__phone")
    def cafe_owner(self, obj):
        return obj.cafe.owner.phone


class ReservationAdmin(admin.ModelAdmin):
    """Menu Item Admin Model"""

    list_display = [
        "full_name",
        "phone",
        "cafe",
        "date",
        "time",
        "cafe_code",
        "cafe_owner",
        "user",
        "state",
    ]
    list_display_links = ["full_name", "phone", "user"]
    list_editable = ["state"]
    list_filter = ["phone", "cafe__code", "cafe__owner__phone", "state"]
    sortable_by = ["full_name", "date", "time"]
    search_fields = [
        "full_name",
        "phone",
        "date",
        "time",
        "cafe__code",
        "cafe__owner__phone",
    ]

    @admin.display(ordering="cafe__code")
    def cafe_code(self, obj):
        return obj.cafe.code

    @admin.display(ordering="cafe__owner__phone")
    def cafe_owner(self, obj):
        return obj.cafe.owner.phone


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    max_num = 1


class OrderAdmin(admin.ModelAdmin):
    """Order Admin Model"""

    list_display = [
        "code",
        "total_price",
        "state",
        "registered_date",
        "delivered_date",
        "user",
        "user_phone",
        "cafe",
        "cafe_code",
        "cafe_owner",
    ]
    list_display_links = ["code", "total_price"]
    list_editable = ["state"]
    list_filter = ["cafe__code", "state"]
    sortable_by = ["registered_date", "code"]
    search_fields = [
        "code",
        "total_price",
        "registered_date",
        "user__phone",
        "cafe__code",
        "cafe__persian_title",
        "cafe__owner__phone",
    ]
    inlines = [OrderItemInline]

    @admin.display(ordering="cafe__code")
    def cafe_code(self, obj):
        return obj.cafe.code

    @admin.display(ordering="cafe__owner__phone")
    def cafe_owner(self, obj):
        return obj.cafe.owner.phone

    @admin.display(ordering="cafe__persian_title")
    def cafe_title(self, obj):
        return obj.cafe.persian_title

    @admin.display(ordering="user__phone")
    def user_phone(self, obj):
        return obj.user.phone


class BartenderAdmin(admin.ModelAdmin):
    list_display = [
        "user_fullname",
        "phone",
        "cafe",
        "cafe_code",
        "is_active",
        "user_last_login",
    ]
    list_editable = ["is_active"]
    list_display_links = ["user_fullname", "phone", "cafe_code"]
    ordering = ["id"]

    list_filter = ["is_active", "cafe"]
    search_fields = ["phone", "cafe_code"]

    @admin.display(ordering="cafe__code")
    def cafe_code(self, obj):
        return obj.cafe.code

    @admin.display(ordering="user__fullName")
    def user_fullname(self, obj):
        return obj.user.fullName

    @admin.display(ordering="user__last_login")
    def user_last_login(self, obj):
        return obj.user.last_login


class CustomerAdmin(admin.ModelAdmin):
    """Customer admin"""

    list_display = ["firstName", "lastName", "phone", "birthdate", "cafe", "cafe_code"]
    list_display_links = ["firstName", "lastName", "phone", "cafe_code"]
    ordering = ["id"]

    list_filter = ["cafe__code"]
    search_fields = ["phone", "cafe__code"]

    @admin.display(ordering="cafe__code")
    def cafe_code(self, obj):
        return obj.cafe.code


class EventAdmin(admin.ModelAdmin):
    """Event admin"""

    list_display = [
        "title",
        "cafe",
        "cafe_code",
        "status",
        "is_expired",
        "created_date",
    ]
    list_display_links = ["title", "cafe", "cafe_code"]
    list_filter = ["cafe__code"]
    search_fields = ["title", "cafe__code"]

    @admin.display(ordering="cafe__code")
    def cafe_code(self, obj):
        return obj.cafe.code


class BranchAdmin(admin.ModelAdmin):
    """Branch admin"""

    list_display = ("id", "latitude", "longitude", "street", "is_active")
    list_filter = ("is_active",)
    search_fields = ("cafe__code", "province__name", "city__name", "street")

    fieldsets = (
        (None, {"fields": ("cafe", "province", "city")}),
        ("Location Information", {"fields": ("latitude", "longitude", "street")}),
        ("Status", {"fields": ("is_active",)}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("cafe", "province", "city")
        return qs


class TableAdmin(admin.ModelAdmin):
    """Table admin"""

    list_display = ("id", "cafe", "number")
    list_display_links = ("id", "cafe")
    list_editable = ("number",)
    search_fields = ("cafe__code",)


admin.site.register(Cafe, CafeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Suggestion, SuggestionAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Bartender, BartenderAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(Table, TableAdmin)
