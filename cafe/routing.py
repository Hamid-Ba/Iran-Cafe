# routing.py
from django.urls import re_path

from cafe.consumers import OrderConsumer, PagerConsumer

websocket_urlpatterns = [
    re_path(r"ws/order/", OrderConsumer.as_asgi()),
    re_path(r"ws/pager/", PagerConsumer.as_asgi()),
]
