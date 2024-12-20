from rest_framework_simplejwt.tokens import RefreshToken

import jwt
import datetime
from django.conf import settings
from ..models import User

TOKEN_EXPIRATION_TIME = datetime.timedelta(hours=1)

def generate_jwt_token(user):
    refresh = RefreshToken.for_user(user)  
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

from rest_framework_simplejwt.tokens import AccessToken
from django.core.exceptions import ObjectDoesNotExist

def decode_jwt(token):
    try:
        payload = AccessToken(token)

        user_id = payload['user_id']

        user = User.objects.get(id=user_id)
        return user

    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired.")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token.")
    except ObjectDoesNotExist:
        raise ValueError("User not found.")

