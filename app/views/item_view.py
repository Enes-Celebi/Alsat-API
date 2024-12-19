from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..serializers.item_serializer import ItemSerializer
from ..services.item_service import create_item

@api_view(['POST'])
def post_item(request):
    if request.method == 'POST':
        serializer = ItemSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            item = create_item(request.user, serializer.validated_data)
            return Response({"message": "Item posted successfully", "item_id": item.id}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)