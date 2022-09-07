from django.contrib import admin
from account.models import User
from cafe.models import Cafe

class CafeAdmin(admin.ModelAdmin):
    """Cafe Admin Model"""
    list_display = ['code' ,'owner','persian_title' , 'english_title' ,'state' , 'type' , 'province' ,'city']
    list_display_links = ['code' , 'owner' , 'persian_title' , 'english_title']
    list_editable = ['state']
    list_filter = ['province' , 'state' , 'type']
    sortable_by = ['state', 'type']
    
    search_fields = ['code' , 'owner' , 'persian_title' , 'english_title']

    fieldsets = (
        ('General Info', {
            'fields': ('code' , 'owner', 'persian_title','english_title' , 'slug' , 'image_url'),
        }),
        ('Status Info', {
            'classes': ('collapse',),
            'fields': ('state', 'type'),
        }),
        ('Contact Info', {
            'classes': ('collapse',),
            'fields': ('phone', 'email', 'telegram_id', 'instagram_id'),
        }),
        ('Address Info', {
            'classes': ('collapse',),
            'fields': ('province', 'city', 'street', 'postal_code' , 'google_map_url'),
        }),
        ('Extra Info', {
            'classes': ('collapse',),
            'fields': ('short_desc', 'desc'),
        }),
    )

admin.site.register(Cafe , CafeAdmin)