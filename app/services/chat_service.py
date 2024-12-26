from ..models import Chat, Message
from django.db import IntegrityError

def start_chat(sender, receiver, item):
    try:
        chat = Chat.objects.create(sender=sender, receiver=receiver, item=item)
        return chat
    except IntegrityError:
        return Chat.objects.get(sender=sender, receiver=receiver, item=item)


def send_message(chat, sender, content):
    message = Message.objects.create(chat=chat, sender=sender, content=content)
    return message


def mark_messages_as_read(chat, receiver):
    messages_to_update = Message.objects.filter(chat=chat, sender__neq=receiver, is_read=False)
    messages_to_update.update(is_read=True)

    return messages_to_update


def get_user_chats(user):
    chats_as_buyer = Chat.objects.filter(sender=user).select_related('item', 'receiver')
    chats_as_seller = Chat.objects.filter(receiver=user).select_related('item', 'sender')
    buyer_chats = [{"chat": chat, "role": "buyer"} for chat in chats_as_buyer]
    seller_chats = [{"chat": chat, "role": "seller"} for chat in chats_as_seller]

    return buyer_chats + seller_chats