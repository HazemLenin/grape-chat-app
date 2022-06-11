from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from core.models import Room, Message


class MessagesWSConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        room_id = self.scope['url_route']['kwargs']['room_id']

        # connect channel to it's group (room)
        await self.channel_layer.group_add(f'room__{room_id}', self.channel_name)
        await self.accept()

    async def receive_json(self, content):
        room_id = self.scope['url_route']['kwargs']['room_id']
        user = self.scope['user']
        message = content['text']

        await self.create_message(room_id, user, message)

        event = {
            'type': 'room_message',
            'username': user.username,
            'text': message
        }

        await self.channel_layer.group_send(f'room__{room_id}', event)

    async def room_message(self, event):
        await self.send_json(event)

    @database_sync_to_async
    def create_message(self, room_id, user, message):
        room = Room.objects.get(id=room_id)

        Message.objects.create(room=room, sender=user, text=message)

    async def disconnect(self, code):
        room_id = self.scope['url_route']['kwargs']['room_id']
        await self.channel_layer.group_discard(f'room__{room_id}', self.channel_name)
        await self.close()
