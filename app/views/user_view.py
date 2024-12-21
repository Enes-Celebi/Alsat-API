from rest_framework import status
from rest_framework.response import Response 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from ..serializers.user_serializer import UserSerializer
from ..services.user_service import get_user_by_id
from app.models import User

@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_by_id_view(request, user_id):
    user = get_user_by_id(user_id)

    if user is None:
        return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)

    serialized_user = UserSerializer(user)
    return Response(serialized_user.data, status=status.HTTP_200_OK)
