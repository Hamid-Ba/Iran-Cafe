from rest_framework.routers import DefaultRouter
from django.urls import (
    path,
    include,
    )

from blog import views


router = DefaultRouter()
router.register('manage-blog' , views.ManageBlogView)

app_name = "blog"

urlpatterns = [
    path("",include(router.urls)), 
    path('cafes/<int:cafe_code>/blogs/',views.CafesBlogListView.as_view()),
    path('iran-cafe/',views.IranCafeBlogsView.as_view()),
    path('<str:slug>/',views.BlogDetailView.as_view()),
    path('all/blogs',views.BlogsView.as_view(),name='all_blogs'),
    path('the_latest_blogs',views.LatestBlogsView.as_view(),name='the_latest_blogs'),
]