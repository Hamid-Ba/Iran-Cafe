from rest_framework.routers import DefaultRouter
from django.urls import (
    path,
    include,
    )

from blog import views


router = DefaultRouter()

app_name = "blog"

urlpatterns = [
    # path("",include(router.urls)), 
    path("create/",views.CreateBlogView.as_view(),name="create_blog"),
]