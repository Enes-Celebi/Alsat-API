from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from ..serializers.chat_serializer import ChatSerializer
from ..serializers.message_serializer import MessageSerializer
from ..services.chat_service import start_chat, send_message
from django.views.decorators.csrf import csrf_exempt
from ..models import Item, Chat, Message

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_chat_view(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)

    sender = request.user
    receiver = item.seller

    chat = start_chat(sender, receiver, item)

    return Response(ChatSerializer(chat).data, status=status.HTTP_201_CREATED)
    

@api_view(['GET'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_chat_messages(request, chat_id):
    try:
        chat = Chat.objects.get(id=chat_id)
    except Chat.DoesNotExist:
        return Response({"error": "Chat not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.user not in [chat.sender, chat.receiver]:
        return Response({"error": "You are not a participant in this chat."}, statis=status.HTTP_403_FORBIDDEN)

    messages = Message.objects.filter(chat=chat).order_by('created_at')
    return Response(MessageSerializer(messages, many=True).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def send_message_view(request, chat_id):
    try: 
        chat = Chat.objects.get(id=chat_id)
    except Chat.DoesNotExist:
        return Response({"error": "Chat not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.user not in [chat.sender, chat.receiver]:
        return Response({"error": "You are not a participant in this chat."}, status=status.HTTP_403_FORBIDDEN)

    content = request.data.get('content')
    if not content:
        return Response({"error": "Message content is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    message = send_message(chat, request.user, content)
    return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)