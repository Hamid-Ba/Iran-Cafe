from rest_framework.routers import DefaultRouter
from django.urls import (
    path,
    include,
    )

from cafe import views


router = DefaultRouter()
router.register('cafes' , views.CafeViewSet)
router.register('menuitems' , views.MenuItemViewSet)
router.register('galleries' , views.GalleryViewSet)
router.register('suggestions' , views.SuggestionView)
router.register('reservations' , views.ReservationViewSet)
router.register('order' , views.OrderViewSet)

app_name = "cafe"

urlpatterns = [
    path("",include(router.urls)),
    path("category_list",views.CategoryView.as_view(),name='category_list'),
    path("menuitem_list/<int:cafe_id>/",views.MenuItemListView.as_view(),name='menuitem_list'),
    path("province_cafes/<str:province_slug>/",views.CafesProvinceListView.as_view(),name='cafes_by_province'),
    path("city_cafes/<str:city_slug>/",views.CafesCityListView.as_view(),name='cafes_by_city'),
    path("cafe_id/<str:cafe_code>/",views.CafeIdView.as_view(),name='cafe_id'),
    path("send_suggest/",views.CreateSuggestionApiView.as_view(),name='send_suggest')
    # path("order/",views.OrderViewSet.as_view(),name='order')
]