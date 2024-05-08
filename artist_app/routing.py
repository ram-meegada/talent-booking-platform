from .consumers import *
from django.urls import path

websocket_urlpatterns = [
    path("chat/<int:user1>/<int:user2>", ChattingConsumer.as_asgi())
]