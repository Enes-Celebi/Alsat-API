import jwt
import datetime
from django.conf import settings
from ..models import User

TOKEN_EXPIRATION_TIME = datetime.timedelta(hours=1)

def generate_jwt_token(user):
    payload = {
        "user_id": user.id,
        "email": user.email,
        "exp": datetime.datetime.utcnow() + TOKEN_EXPIRATION_TIME,
        'iat': datetime.datetime.utcnow() 
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token

def decode_jwt(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user = User.objects.get(id=payload['user_id'])
        return user
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    except User.DoesNotExist:
        return None
