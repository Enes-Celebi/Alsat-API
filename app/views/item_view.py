from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from ..serializers.item_serializer import ItemSerializer
from ..services.item_service import create_item
from ..utils.jwt_util import decode_jwt

@api_view(['POST'])
def post_item(request):
    if request.method == 'POST':
        token = request.headers.get('Authorization', '').split(' ')[-1]

        if not token: 
            return Response({"error": "Token is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = decode_jwt(token)
        
        if not user:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = ItemSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            item = create_item(user, serializer.validated_data)
            return Response({"message": "Item posted successfully", "item_id": item.id}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)