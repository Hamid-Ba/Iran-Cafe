from rest_framework.routers import DefaultRouter
from django.urls import (
    path,
    include,
    )

from comment import views


router = DefaultRouter()
# router.register('comments' , views.CommentViewSet , basename='comment')

app_name = "comment"

urlpatterns = [
    # path("",include(router.urls)), 
    path("create/",views.CreateCommentView.as_view(),name="create_comment"),
    path("item_comments/<int:item_id>",views.MenuItemCommentView.as_view(),name="item_comments"),
    path("comment/<int:id>",views.SingleCommentView.as_view(),name="comment"),
    path("response_comment",views.ResponseCommentView.as_view(),name="response"),
]