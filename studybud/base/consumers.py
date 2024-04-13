from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Room, Message

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'                
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )        
    
    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON data: {e}")
            return
        message = text_data_json['message']
        username = text_data_json['username']
        room = await self.get_room()        
        await Message.objects.acreate(
            user=self.scope['user'],
            room=room,
            body=message
        )        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']                
        await self.send(text_data= json.dumps({
            'message': message,
            'username': username,
            'meetoo': 'ok'
        }))

    async def get_room(self):
        if not hasattr(self, '_room'):
            self._room = await Room.objects.aget(id=self.room_id)
        return self._room
        