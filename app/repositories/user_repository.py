from app.models import User
import bcrypt

def create_user(email, password, full_name=None):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    user = User(email=email, password=hashed_password, full_name=full_name)
    user.save()
    return user

def get_user_by_email(email):
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None