from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Room, Message
from .api.serializers import RoomMessagesSerializer
from .serializers import UserSerializer
from django.db.models import Q
from channels.db import database_sync_to_async


@database_sync_to_async
def check_user_in_participants(room, user):
    # Check if the user is in the participants of the room
    return not room.participants.filter(
        Q(id=user.id)
    ).exists(), room.participants.count()


@database_sync_to_async
def serialize_user(user):
    return UserSerializer(user, many=False).data


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_id}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON data: {e}")
            return
        message = text_data_json["message"]
        user = self.scope["user"]
        room = await self.get_room()
        new_message = await Message.objects.acreate(user=user, room=room, body=message)
        new_participant, participant_count = await check_user_in_participants(
            room, user
        )
        if new_participant:
            await room.participants.aadd(user)
            response = {
                "type": "chat_message",
                "message": RoomMessagesSerializer(new_message, many=False).data,
                "is_new_participant": new_participant,
                "participant_count": participant_count + 1,
                "user": await serialize_user(user),
            }
        else:
            response = {
                "type": "chat_message",
                "message": RoomMessagesSerializer(new_message, many=False).data,
                "is_new_participant": new_participant,
            }
        await self.channel_layer.group_send(self.room_group_name, response)

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        is_new_participant = event["is_new_participant"]
        if is_new_participant:
            participant_count = event["participant_count"]
            user = event["user"]
            response = json.dumps(
                {
                    "message": message,
                    "is_new_participant": is_new_participant,
                    "participant_count": participant_count,
                    "user": user,
                }
            )
        else:
            response = json.dumps(
                {"message": message, "is_new_participant": is_new_participant}
            )
        await self.send(text_data=response)

    async def get_room(self):
        if not hasattr(self, "_room"):
            self._room = await Room.objects.aget(id=self.room_id)
        return self._room
