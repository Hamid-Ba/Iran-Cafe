from rest_framework.routers import DefaultRouter
from django.urls import (
    path,
    include,
    )

from cafe import views


router = DefaultRouter()
router.register('' , views.CafeViewSet)
# router.register('' , views.CategoryView , basename='cafe')

app_name = "cafe"

urlpatterns = [
    path("",include(router.urls)),
    path("category_list",views.CategoryView.as_view(),name='category_list'),
    path("province_cafes/<str:province_slug>/",views.CafesProvinceListView.as_view(),name='cafes_by_province'),
    path("city_cafes/<str:city_slug>/",views.CafesCityListView.as_view(),name='cafes_by_city')
]