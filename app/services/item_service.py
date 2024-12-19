from ..models import Item  

def create_item(user, validated_data):
    item = Item.objects.create(seller=user, **validated_data)
    return item