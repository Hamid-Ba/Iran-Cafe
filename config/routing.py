from channels.routing import ProtocolTypeRouter, URLRouter

from cafe.routing import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "websocket": URLRouter(websocket_urlpatterns),
    }
)
