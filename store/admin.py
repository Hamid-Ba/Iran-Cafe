from django.contrib import admin
from store import models

# Register your models here.


class StoreCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "sortitem", "sub_category")
    list_filter = ("sub_category",)


admin.site.register(models.StoreCategory, StoreCategoryAdmin)
