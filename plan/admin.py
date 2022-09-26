"""
Plan Module Admin Models
"""
from django.contrib import admin
from plan.models import *

class PlanAdmin(admin.ModelAdmin):
    """Plan Admin Model"""
    list_display = ['title' ,'period','price' , 'is_active']
    list_display_links = ['title' , 'period' , 'price']
    list_editable = ['is_active']
    list_filter = ['is_active']
    sortable_by = ['period', 'price']

admin.site.register(Plan, PlanAdmin)