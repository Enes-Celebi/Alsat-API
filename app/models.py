from django.db import models
from django.utils.timezone import now

class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    full_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=now)

    class Meta:
        db_table = "users" 
        managed = True  

    def __str__(self):
        return self.email


class Item(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "items"
        managed = True

    def __str__(self):
        return f"{self.title} by {self.seller.full_name}"


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')  
    image = models.ImageField(upload_to='item_images/')

    class Meta:
        db_table = "item_images"
        managed = True

    def __str__(self):
        return f"Image for {self.item.title}" 


class Chat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_chats')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_chats')  
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta: 
        db_table = "chats"
        managed = True
        unique_together = ['sender', 'receiver', 'item']

    def __str__(self):
        item_name = self.item.title if self.item and not self.item.is_deleted else "Deleted Item"  
        return f"Chat between {self.sender.email} and {self.receiver.email} about {item_name}"


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_sent')  
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "messages"
        managed = True

    def __str__(self):
        return f"Message from {self.sender.email} in chat {self.chat.id}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "favorites"
        managed = True

    def __str__(self):
        return f"{self.user.email} favorited {self.item.title}"
