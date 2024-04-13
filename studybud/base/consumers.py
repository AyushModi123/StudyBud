from channels.generic.websocket import WebsocketConsumer
import json
from .models import Room, Message

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        # self.room_group_name = f'chat_{self.room_id}'
        print(self.room_id)
        # Join room group
        # await self.channel_layer.group_add(
        #     self.room_group_name,
        #     self.channel_name
        # )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        # self.channel_layer.group_discard(
        #     self.room_group_name,
        #     self.channel_name
        # )
        self.close()

    # Receive message from WebSocket
    def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON data: {e}")
            return
        message = text_data_json['message']
        username = text_data_json['username']

        # Save the message to the database
        room = self.get_room()
        Message.objects.create(
            user=self.scope['user'],
            room=room,
            body=message
        )

        # Send message to room group
        # self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'chat_message',
        #         'message': message,
        #         'username': username
        #     }
        # )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    def get_room(self):
        if not hasattr(self, '_room'):
            self._room = Room.objects.aget(id=self.room_id)
        return self._room
        