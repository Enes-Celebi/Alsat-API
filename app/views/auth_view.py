from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny  
from rest_framework import status
from rest_framework.response import Response
from app.services.auth_service import signup, signin
from app.serializers.user_serializer import UserSerializer
from app.utils.jwt_util import generate_jwt_token

@api_view(['POST'])
@permission_classes([AllowAny])  
def signup_view(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        full_name = request.data.get('full_name', None)

        if not email or not password:
            return Response({"error": "Email and password are required!"}, status=status.HTTP_400_BAD_REQUEST)
        
        try: 
            user = signup(email, password, full_name)
            user_data = UserSerializer(user).data
            return Response({"message": "User created successfully", "user": user_data}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "An unexpected error occurred.", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])  
def signin_view(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error": "Email and password are required!"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user, _ = signin(email, password)
            tokens = generate_jwt_token(user)
            return Response({
                "message": "Login successful",
                "user_id": user.id,
                "token": tokens
            }, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "error": "An unexpected error occurred.", 
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
