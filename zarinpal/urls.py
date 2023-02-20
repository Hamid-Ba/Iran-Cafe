from rest_framework.routers import DefaultRouter
from django.urls import (
    path,
    include,
)
from . import views


router = DefaultRouter()
router.register("cafes", views.CafesPaymentsView)

app_name = "payment"

urlpatterns = [
    path("", include(router.urls)),
    path(
        "place_order/<int:plan_id>/", views.PlaceOrderView.as_view(), name="place_order"
    ),
    path("verify_order/", views.VerifyOrderView.as_view(), name="verify_order"),
]
