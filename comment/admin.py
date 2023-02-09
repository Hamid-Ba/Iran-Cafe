from django.contrib import admin

from comment.models import Comment


# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    """Comment Admin Model"""

    list_display = ["user", "date", "is_cafe"]
    list_display_links = ["user", "date", "is_cafe"]

    list_filter = ["is_cafe"]
    sortable_by = ["user", "is_cafe", "date"]

    search_fields = ["user"]


admin.site.register(Comment, CommentAdmin)
