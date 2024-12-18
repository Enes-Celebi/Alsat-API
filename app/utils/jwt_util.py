import jwt
import datetime
from django.conf import settings

TOKEN_EXPIRATION_TIME = datetime.timedelta(hours=1)

def generate_jwt_token(user):
    payload = {
        "user_id": user.id,
        "email": user.email,
        "exp": datetime.datetime.utcnow() + TOKEN_EXPIRATION_TIME
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorith="H256")
    return token