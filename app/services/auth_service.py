import bcrypt
import logging
from app.repositories.user_repository import create_user, get_user_by_email
from app.utils.jwt_util import generate_jwt_token

logger = logging.getLogger(__name__)

def signup(email, password, full_name=None):
    if get_user_by_email(email):
        raise ValueError("User with this email already exists.")

    return create_user(email=email, password=password, full_name=full_name)

def signin(email, password):
    user = get_user_by_email(email)

    print("User found:", user)

    if not user:
        raise ValueError("Invalid email or password.")
    
    print("Stored password hash:", user.password)

    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        print("Password is correct!")
    else:
        print("Password mismatch!")  
        raise ValueError("Invalid email or password.")
    
    return user
