"""
site info module admin models
"""
from jalali_date.admin import ModelAdminJalaliMixin
from django.contrib import admin

from siteinfo.models import AboutUs, ContactUs, Robots, Error


class AboutUsAdmin(admin.ModelAdmin):
    """About Us Admin Model"""

    list_display = ["id", "phones", "address"]
    list_display_links = ["id", "phones", "address"]

    fieldsets = (
        (
            "Contact Info",
            {
                "classes": ("collapse",),
                "fields": ("phones", "emails"),
            },
        ),
        (
            "Address Info",
            {
                "classes": ("collapse",),
                "fields": ("address",),
            },
        ),
        (
            "Extra Info",
            {
                "classes": ("collapse",),
                "fields": ("text",),
            },
        ),
    )


class ContactUsAdmin(admin.ModelAdmin):
    """Contact Us Admin Model"""

    list_display = ["id", "full_name", "phone"]
    list_display_links = ["id", "full_name", "phone"]
    search_fields = ["full_name", "phone"]


class RobotsAdmin(admin.ModelAdmin):
    """Robots Admin Model"""

    list_display = ["id", "name"]
    list_display_links = ["id", "name"]

class ErrorAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    """Error Admin Model"""
    
    list_display = ["id", "time_raised", "reference", "status"]
    list_display_links = ["id", "reference", "status"]

admin.site.register(AboutUs, AboutUsAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(Robots, RobotsAdmin)
admin.site.register(Error, ErrorAdmin)
