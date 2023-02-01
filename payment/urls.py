from rest_framework.routers import DefaultRouter
from django.urls import (
    path,
    include,
    )
from . import views

urlpatterns = [
    path('place_order/<int:plan_id>/',views.MakePaymentView.as_view(),name='place_order'),
]