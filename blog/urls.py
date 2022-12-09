from rest_framework.routers import DefaultRouter
from django.urls import (
    path,
    include,
    )

from blog import views


router = DefaultRouter()
router.register('blog' , views.ManageBlogView)

app_name = "blog"

urlpatterns = [
    path("",include(router.urls)), 
    path('cafes/<int:cafe_id>/blogs/',views.CafesBlogListView.as_view())
    # path("create/",views.CreateBlogView.as_view(),name="create_blog"),
]