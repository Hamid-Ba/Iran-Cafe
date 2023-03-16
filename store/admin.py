from django.contrib import admin
from store import models

# Register your models here.


class StoreCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "sortitem", "sub_category")
    list_filter = ("sub_category",)


class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "category")
    list_filter = ("category",)
    search_fields = ["title"]


class StoreOrderItemInline(admin.TabularInline):
    model = models.StoreOrderItem
    extra = 1


class StoreOrderAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "state",
        "total_price",
        "phone",
        "address",
        "postal_code",
        "cafe",
    )
    inlines = [
        StoreOrderItemInline,
    ]


class StoreOrderItemAdmin(admin.ModelAdmin):
    list_display = ("order_id", "title", "desc", "price", "count", "image_url")


admin.site.register(models.StoreCategory, StoreCategoryAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.StoreOrder, StoreOrderAdmin)
# admin.site.register(models.StoreOrderItem, StoreOrderItemAdmin)
