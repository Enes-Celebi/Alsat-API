from ..models import Item  
from django.core.exceptions import ObjectDoesNotExist

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


def fetch_user_items(user_id=None, authenticated_user=None):
    if user_id is None and authenticated_user is None:
        raise ValueError("Either user_id or authenticated_user must be provided.")

    if user_id is None:
        user_id = authenticated_user.id

    try:
        items = Item.objects.filter(seller_id=user_id, is_deleted=False)
    except Item.DoesNotExist:
        return None

    return items

