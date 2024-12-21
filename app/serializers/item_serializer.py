from rest_framework import serializers
from ..models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'title', 'description', 'price', 'is_deleted', 'seller_id']  

    def create(self, validated_data):
        user = self.context['request'].user  
        item = Item.objects.create(seller=user, **validated_data)
        return item
