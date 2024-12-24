from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from ..serializers.item_serializer import ItemSerializer
from ..services.item_service import create_item, get_items_filtered, fetch_user_items, update_user_item, delete_user_item, get_item_by_id
from ..utils.jwt_util import decode_jwt
from app.models import Item

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
    sort = request.query_params.get('sort', None)

    items = get_items_filtered(title=title, min_price=min_price, max_price=max_price)

    if sort == "low_to_high":
        items = items.order_by("price")
    elif sort == "high_to_low":
        items = items.order_by("-price")
    elif sort == "newest":
        items = items.order_by("-created_at")

    serializer = ItemSerializer(items, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PATCH'])
@permission_classes([AllowAny])
def user_items_view(request, user_id=None, item_id=None):
    if request.method == 'GET':
        try:
            if user_id is None:
                if not request.user.is_authenticated:
                    return Response({"error": "Authentication required to view your listing"}, status=status.HTTP_401_UNAUTHORIZED)
                
                items = fetch_user_items(authenticated_user=request.user)
            else: 
                items = fetch_user_items(user_id=user_id)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if not items.exists():
            return Response({"error": "No items found."}, status=status.HTTP_404_NOT_FOUND)
        
        serialized_items = ItemSerializer(items, many=True)
        return Response(serialized_items.data, status=status.HTTP_200_OK)

    elif request.method == 'PATCH':
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required to update an item."}, status=status.HTTP_401_UNAUTHORIZED)

        if item_id is None:
            return Response({"error": "Item ID is required to update an item."}, status=status.HTTP_201_CREATED)

        try:
            update_data = request.data
            updated_item = update_user_item(item_id=item_id, user=request.user, update_data=update_data)

            serialized_item = ItemSerializer(updated_item)
            return Response(serialized_item.data, status=status.HTTP_200_OK)

        except Item.DoesNotExist as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": f"An unknown error occured: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_item_view(request, item_id):
    try: 
        item = delete_user_item(item_id, request.user)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
    except PermissionError as e:
        return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

    return Response({"message": "Item successfully deleted."}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_item_by_id_view(request, item_id):
    item = get_item_by_id(item_id)

    if item is None:
        return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)

    serialized_item = ItemSerializer(item)
    return Response(serialized_item.data, status=status.HTTP_200_OK) 