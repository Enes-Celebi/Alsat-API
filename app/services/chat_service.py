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