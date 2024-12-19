from ..models import Item  

def create_item(user, validated_data):
    item = Item.objects.create(seller=user, **validated_data)
    return item

def get_items_filtered(title=None, min_price=None, max_price=None):
    items = Item.objects.all()

    if title: 
        items = items.filter(title__icontains=title)
    if min_price:
        items = items.filter(price__gte=min_price)
    if max_price:
        items = items.filter(price__lte=max_price)

    return items