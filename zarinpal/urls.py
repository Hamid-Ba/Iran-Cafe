from rest_framework.routers import DefaultRouter
from django.urls import (
    path,
    include,
)
from . import views


router = DefaultRouter()
router.register("cafes", views.CafesPaymentsView)
router.register("cafes_store", views.CafesStorePaymentsView)

app_name = "payment"

urlpatterns = [
    path("", include(router.urls)),
    path(
        "place_order/<int:plan_id>/", views.PlaceOrderView.as_view(), name="place_order"
    ),
    path("verify_order/", views.VerifyOrderView.as_view(), name="verify_order"),
    path(
        "place_store_order/<int:order_id>/",
        views.PlaceStoreOrderView.as_view(),
        name="place_store_order",
    ),
    path(
        "verify_store_order/",
        views.VerifyStoreOrderView.as_view(),
        name="verify_store_order",
    ),
]
