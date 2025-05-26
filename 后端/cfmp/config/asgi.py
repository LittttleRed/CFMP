"""
ASGI config for cfmp project.

It exposes the ASGI callable as a models-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""


import os
from channels.routing import ProtocolTypeRouter,URLRouter
from django.core.asgi import get_asgi_application


django_asgi_app = get_asgi_application()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import user.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket":
        URLRouter(
            # 在这里添加你的WebSocket路由
            user.routing.websocket_urlpatterns
        )
})