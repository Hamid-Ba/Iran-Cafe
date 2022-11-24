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
    path("create/",views.CreateCommentView.as_view(),name="create_comment")
]