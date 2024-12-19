from rest_framework import serializers
from ..models import Chat
from .user_serializer import UserSerializer
from .item_serializer import ItemSerializer

class ChatSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver UserSerializer(read_only=True)
    item = ItemSerializer(read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'sender', 'receiver', 'item', 'created_at']