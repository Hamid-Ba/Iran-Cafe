# routing.py
from django.urls import re_path

from cafe.consumers import OrderConsumer

websocket_urlpatterns = [
    re_path(r"ws/order/", OrderConsumer.as_asgi()),
]
