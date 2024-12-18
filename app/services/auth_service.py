import bcrypt
from app.repositories.user_repository import create_user, get_user_by_email

def signup(email, password, full_name=None):
    if get_user_by_email(email):
        raise ValueError("User with this email already exists.")

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    return create_user(email=email, password=hashed_password, full_name=full_name)

