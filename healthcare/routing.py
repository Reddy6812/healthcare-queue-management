from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from channels.auth import AuthMiddlewareStack
from appointments.consumers import QueueConsumer

websocket_urlpatterns = [
    re_path(r'ws/queue/(?P<doctor_id>\d+)/$', QueueConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
