from django.contrib import admin

from cloud import models


class CloudyCustomerAdminModel(admin.ModelAdmin):
    """Cloudy Customer Admin Model"""

    list_display = [
        "id",
        "cafe",
        "fullName",
        "is_called",
        "is_confirmed",
        "is_deployed",
        "is_cancelled",
        "created_date",
    ]

    list_display_links = ["id", "cafe"]
    list_filter = ["is_called", "is_confirmed", "is_deployed", "is_cancelled"]
    list_editable = ["is_called", "is_confirmed", "is_deployed", "is_cancelled"]
    search_fields = ["cafe", "fullName"]


admin.site.register(models.CloudyCustomer, CloudyCustomerAdminModel)
