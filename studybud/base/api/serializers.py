from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from base.models import Room, Message


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class RoomMessagesSerializer(ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Message
        fields = '__all__'