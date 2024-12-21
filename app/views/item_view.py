from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from ..serializers.item_serializer import ItemSerializer
from ..services.item_service import create_item, get_items_filtered, fetch_user_items
from ..utils.jwt_util import decode_jwt

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_item(request):
    user = request.user  
    serializer = ItemSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        item = create_item(user, serializer.validated_data)
        return Response({"message": "Item posted successfully", "item_id": item.id}, 
                      status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([AllowAny])
def get_items(request):
    title = request.query_params.get('title', None)
    min_price = request.query_params.get('min_price', None)
    max_price = request.query_params.get('max_price', None)

    items = get_items_filtered(title=title, min_price=min_price, max_price=max_price)

    serializer = ItemSerializer(items, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_items(request, user_id=None):
    try:
        if user_id is None:
            # No user_id passed in the URL, fetch items for the authenticated user
            items = fetch_user_items(authenticated_user=request.user)
        else:
            # user_id passed in the URL, fetch items for the specified user
            items = fetch_user_items(user_id=user_id)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # Check if items exist
    if not items.exists():
        return Response({"error": "No items found."}, status=status.HTTP_404_NOT_FOUND)

    # Serialize and return the items
    serialized_items = ItemSerializer(items, many=True)
    return Response(serialized_items.data, status=status.HTTP_200_OK)




