from django.urls import path, re_path
from . import consumers
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

websocket_urlpatterns = [
    #path('ws/chat/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'websocket/ws/notifications/', consumers.NotificationConsumer.as_asgi()),    
]

application = ProtocolTypeRouter({
    "websocket": URLRouter(websocket_urlpatterns),
})
