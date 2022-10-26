from rest_framework.routers import DefaultRouter
from django.urls import (
    path,
    include,
    )

from queries import views

app_name = 'queries'

urlpatterns = [
    path('order/' , views.OrderQueryView.as_view(), name='order')
]