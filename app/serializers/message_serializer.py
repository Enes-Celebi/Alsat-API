from rest_framework import serializers
from ..models import Message
from .user_serializer import UserSerializer
from .item_serializer import ItemSerializer

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=true)
    chat = ChatSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'chat', 'content', 'is_read', 'created_at']