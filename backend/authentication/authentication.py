from backend.database.db_utils import get_user
from encryption import verify_password
from backend.models.user import User

def authenticate_user(email: str, password: str) -> User | None:
    user = get_user(email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


