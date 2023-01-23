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
router.register('bartender' , views.BartenderViewSet)
router.register('customer' , views.CustomerViewSet)
router.register('events' , views.EventModelViewSet)

app_name = "cafe"

urlpatterns = [
    path("",include(router.urls)),
    path("category_list",views.CategoryView.as_view(),name='category_list'),
    path("menuitem_list/<int:cafe_id>/",views.MenuItemListView.as_view(),name='menuitem_list'),
    path("province_cafes/<str:province_slug>/",views.CafesProvinceListView.as_view(),name='cafes_by_province'),
    path("cafes_search/",views.CafesSearchView.as_view(),name='cafes_search'),
    path("city_cafes/<str:city_slug>/",views.CafesCityListView.as_view(),name='cafes_by_city'),
    path("cafe_detail/<str:cafe_code>/",views.CafeIdView.as_view(),name='cafe_id'),
    path("cafe_detail_page/<int:cafe_id>/",views.CafeDetailView.as_view(),name='cafe_detail_page'),
    path("fast_register/",views.CafeFastRegisterView.as_view(),name='fast_register'),
    path("send_suggest/",views.CreateSuggestionApiView.as_view(),name='send_suggest'),  
    path("user_clubs/",views.UserClubsView.as_view(),name='user_clubs'),
    path("cafe_events/<int:cafe_id>/",views.CafesEventView.as_view(),name='cafe_events'),
    path("cafe_event/<int:pk>/",views.SingleEventView.as_view(),name='single_event'),
]