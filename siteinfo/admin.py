"""
site info module admin models
"""
from django.contrib import admin

from siteinfo.models import AboutUs

class AboutUsAdmin(admin.ModelAdmin):
    """About Us Admin Model"""
    list_display = ['id' ,'phones','address']
    list_display_links = ['id' ,'phones','address']
    
    fieldsets = (
        ('Contact Info', {
            'classes': ('collapse',),
            'fields': ('phones', 'emails'),
        }),
        ('Address Info', {
            'classes': ('collapse',),
            'fields': ('address',),
        }),
        ('Extra Info', {
            'classes': ('collapse',),
            'fields': ('text',),
        }),
    )

admin.site.register(AboutUs, AboutUsAdmin)