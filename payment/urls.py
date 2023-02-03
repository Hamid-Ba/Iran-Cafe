from rest_framework.routers import DefaultRouter
from django.urls import (
    path,
    include,
    )
from . import views

urlpatterns = [
    path('place_order/<int:plan_id>/',views.PlaceOrderView.as_view(),name='place_order'),
    path('verify_order/',views.VerifyOrderView.as_view(),name='verify_order'),
]