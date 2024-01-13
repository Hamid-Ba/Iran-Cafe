# routing.py
from django.urls import re_path

from cafe.consumers import OrderConsumer, PagerConsumer

websocket_urlpatterns = [
    re_path(r"ws/order/(?P<cafe_id>\d+)/$", OrderConsumer.as_asgi()),
    re_path(r"ws/pager/(?P<cafe_id>\d+)/$", PagerConsumer.as_asgi()),
]
