from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.utils.timesince import timesince
from base.models import Room, Message


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class RoomMessagesSerializer(ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    avatar_url = serializers.CharField(source='user.avatar.url', read_only=True)
    timesince = serializers.SerializerMethodField()

    def get_timesince(self, obj):
        return f"{timesince(obj.created)} ago"
    
    class Meta:
        model = Message
        fields = '__all__'