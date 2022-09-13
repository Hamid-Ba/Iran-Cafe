from django.contrib import admin
from account.models import User
from cafe.models import Cafe, Category

class CafeAdmin(admin.ModelAdmin):
    """Cafe Admin Model"""
    list_display = ['code' ,'owner','persian_title' , 'english_title' , 'view_count' ,'state' , 'type' , 'province' ,'city']
    list_display_links = ['code' , 'owner' , 'persian_title' , 'english_title']
    list_editable = ['state']
    list_filter = ['province' , 'state' , 'type']
    sortable_by = ['state', 'type','view_count']
    
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
            'fields': ('desc',),
        }),
    )

class CategoryAdmin(admin.ModelAdmin):
    """Cafe Admin Model"""
    list_display = ['title']
    list_display_links = ['title']
    sortable_by = ['title']

admin.site.register(Cafe , CafeAdmin)
admin.site.register(Category , CategoryAdmin)