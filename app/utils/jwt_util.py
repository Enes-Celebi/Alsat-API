import jwt
import datetime
from django.conf import settings

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
