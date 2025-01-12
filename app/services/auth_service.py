import bcrypt
import logging
from app.repositories.user_repository import create_user, get_user_by_email
from app.utils.jwt_util import generate_jwt_token, generate_refresh_token, decode_refresh_token

logger = logging.getLogger(__name__)

def signup(email, password, full_name=None):
    if get_user_by_email(email):
        raise ValueError("User with this email already exists.")

    return create_user(email=email, password=password, full_name=full_name)


def signin(email, password):
    user = get_user_by_email(email)

    if not user:
        raise ValueError("Invalid email or password.")

    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        token = generate_jwt_token(user)
        return user, token
    else:
        raise ValueError("Invalid email or password.")
    
    return user


def refresh_access_token(refresh_token):
    user = decode_refresh_token(refresh_token)
    if user:
        return generate_jwt_token(user)
    else:
        raise ValueError("Invalid or expired refresh token.")


def logout_user(response):
    response.delete_cookie('refresh_token', httponly=True, secure=True)
    response.delete_cookie('access_token', httponly=True, secure=True)