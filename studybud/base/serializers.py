from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from base.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["avatar", "id", "name", "username"]
