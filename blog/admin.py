from django.contrib import admin
from blog import models


class BlogAdmin(admin.ModelAdmin):
    """Category Admin Model"""
    list_display = ['title','publish_date','is_cafe','user']
    list_display_links = ['title','publish_date']
    sortable_by = ['title','publish_date','is_cafe']

admin.site.register(models.Blog,BlogAdmin)