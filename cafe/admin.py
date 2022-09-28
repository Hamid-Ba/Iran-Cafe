from django.contrib import admin
from cafe.models import Cafe, Category, Gallery, MenuItem, Order, OrderItem, Reservation, Suggestion

class CafeAdmin(admin.ModelAdmin):
    """Cafe Admin Model"""
    list_display = ['code' ,'owner','persian_title' , 'english_title' , 'charge_expired_date' , 'view_count' ,'state' , 'type' , 'province' ,'city']
    list_display_links = ['code' , 'owner' , 'persian_title' , 'english_title']
    list_editable = ['state']
    list_filter = ['province' , 'state' , 'type' , 'charge_expired_date']
    sortable_by = ['state', 'type','view_count' , 'charge_expired_date']
    
    search_fields = ['code' , 'owner__fullName' , 'persian_title' , 'english_title']

    fieldsets = (
        ('General Info', {
            'fields': ('code' , 'owner', 'persian_title','english_title'  , 'image_url'),
        }),
        ('Status Info', {
            'classes': ('collapse',),
            'fields': ('state', 'type' , 'charge_expired_date'),
        }),
        ('Contact Info', {
            'classes': ('collapse',),
            'fields': ('phone', 'email', 'telegram_id', 'instagram_id'),
        }),
        ('Address Info', {
            'classes': ('collapse',),
            'fields': ('province', 'city', 'street' , 'google_map_url'),
        }),
        ('Extra Info', {
            'classes': ('collapse',),
            'fields': ('desc',),
        }),
    )

class CategoryAdmin(admin.ModelAdmin):
    """Category Admin Model"""
    list_display = ['title']
    list_display_links = ['title']
    sortable_by = ['title']

class MenuItemAdmin(admin.ModelAdmin):
    """Menu Item Admin Model"""
    list_display = ['title','price', 'cafe', 'cafe_code','cafe_owner','is_active']
    list_display_links = ['title','price']
    list_editable = ['is_active']
    list_filter = ['is_active' ,'cafe__code','cafe__owner__phone']
    sortable_by = ['title', 'price']
    search_fields = ['title' , 'cafe__code' , 'cafe__owner__phone']
    @admin.display(ordering='cafe__code')
    def cafe_code(self, obj):
        return obj.cafe.code

    @admin.display(ordering='cafe__owner__phone')
    def cafe_owner(self, obj):
        return obj.cafe.owner.phone  

class GalleryAdmin(admin.ModelAdmin):
    """Gallery Admin Model"""
    list_display = ['id','title','cafe','cafe_code','cafe_owner']
    list_display_links = ['id','title']
    list_filter = ['cafe__code','cafe__owner__phone']
    sortable_by = ['title']
    search_fields = ['title' , 'cafe__code' , 'cafe__owner__phone']
    @admin.display(ordering='cafe__code')
    def cafe_code(self, obj):
        return obj.cafe.code

    @admin.display(ordering='cafe__owner__phone')
    def cafe_owner(self, obj):
        return obj.cafe.owner.phone

class SuggestionAdmin(admin.ModelAdmin):
    """Suggestion Admin Model"""
    list_display = ['id','full_name','cafe','cafe_code','cafe_owner']
    list_display_links = ['id','full_name']
    list_filter = ['cafe__code','cafe__owner__phone']
    sortable_by = ['id', 'full_name']
    search_fields = ['full_name' , 'cafe__code' , 'cafe__owner__phone']
    @admin.display(ordering='cafe__code')
    def cafe_code(self, obj):
        return obj.cafe.code

    @admin.display(ordering='cafe__owner__phone')
    def cafe_owner(self, obj):
        return obj.cafe.owner.phone

class ReservationAdmin(admin.ModelAdmin):
    """Menu Item Admin Model"""
    list_display = ['full_name','phone', 'cafe','date','time', 'cafe_code','cafe_owner','user','state']
    list_display_links = ['full_name','phone','user']
    list_editable = ['state']
    list_filter = ['phone','cafe__code','cafe__owner__phone','state']
    sortable_by = ['full_name', 'date','time']
    search_fields = ['full_name' , 'phone' , 'date', 'time' , 'cafe__code' , 'cafe__owner__phone']
    @admin.display(ordering='cafe__code')
    def cafe_code(self, obj):
        return obj.cafe.code

    @admin.display(ordering='cafe__owner__phone')
    def cafe_owner(self, obj):
        return obj.cafe.owner.phone  

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    max_num = 1

class OrderAdmin(admin.ModelAdmin):
    """Order Admin Model"""
    list_display = ['code','total_price' , 'state', 'registered_date' , 'user' , 'user_phone' ,'cafe','cafe_code','cafe_owner']
    list_display_links = ['code','total_price']
    list_editable = ['state']
    list_filter = ['code','cafe__code','state']
    sortable_by = ['registered_date', 'code']
    search_fields = ['code' , 'total_price' , 'registered_date', 'user__phone' , 'cafe__code' , 'cafe__owner__phone']
    inlines = [OrderItemInline]
      
    @admin.display(ordering='cafe__code')
    def cafe_code(self, obj):
        return obj.cafe.code

    @admin.display(ordering='cafe__owner__phone')
    def cafe_owner(self, obj):
        return obj.cafe.owner.phone  

    @admin.display(ordering='user__phone')
    def user_phone(self, obj):
        return obj.user.phone

admin.site.register(Cafe , CafeAdmin)
admin.site.register(Category , CategoryAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Suggestion, SuggestionAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Order, OrderAdmin)