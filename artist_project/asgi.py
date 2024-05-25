"""
ASGI config for artist_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import artist_app.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artist_project.settings')
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack
        (
            URLRouter(                
                artist_app.routing.websocket_urlpatterns
            )
        )
})