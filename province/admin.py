from django.contrib import admin

from province.models import (Province,City)
# Register your models here.

class CityAdmin(admin.ModelAdmin):
    list_display = ['name','province']
    list_display_links = ['name']
    list_filter = ['province']

admin.site.register(Province)
admin.site.register(City,CityAdmin)