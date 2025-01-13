from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from app.services.auth_service import signup, signin, refresh_access_token, logout_user
from app.serializers.user_serializer import UserSerializer
import datetime

REFRESH_TOKEN_EXPIRATION = datetime.timedelta(days=7)

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

from rest_framework.response import Response

@api_view(['POST'])
@permission_classes([AllowAny])  
def signin_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({"error": "Email and password are required!"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user, tokens = signin(email, password)

        return Response({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.full_name
            }
        }, status=status.HTTP_200_OK, headers={
            "Set-Cookie": f"refresh_token={tokens['refresh']}; HttpOnly; Secure; Path=/; Max-Age={REFRESH_TOKEN_EXPIRATION}",
            "Set-Cookie": f"access_token={tokens['access']}; HttpOnly; Secure; Path=/;"
        })
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": "An unexpected error occurred.", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_access_token_view(request):
    refresh_token = request.COOKIES.get('refresh_token')

    if not refresh_token:
        return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        tokens = refresh_access_token(refresh_token) 
        response = HttpResponse({"message": "Access token refreshed", "token": tokens})
        response.set_cookie('access_token', tokens['access'], httponly=True, secure=True)
        return response
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": "An unexpected error occurred.", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def logout_view(request):
    response = HttpResponse({"message": "Logged out successfully"})
    logout_user(response)
    return response
