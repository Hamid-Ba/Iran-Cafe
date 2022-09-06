from django.contrib import admin

from province.models import (Province,City)
# Register your models here.

class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    list_display_links = ['id','name']

class CityAdmin(admin.ModelAdmin):
    list_display = ['id','name','province']
    list_display_links = ['name']
    list_filter = ['province']

admin.site.register(Province,ProvinceAdmin)
admin.site.register(City,CityAdmin)