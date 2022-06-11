from django.urls import path
from . import consumers

ws_urlpatterns = [
    path('rooms/<int:room_id>/', consumers.MessagesWSConsumer.as_asgi()),
]