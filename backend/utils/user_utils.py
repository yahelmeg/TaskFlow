from sqlmodel import Session, select
from backend.models.user import User

def email_exists(email:str, db : Session ) -> bool:
    statement = select(User).where(User.email == email)
    user = db.exec(statement).first()
    if user:
        return True
    return False

def get_user_by_id( user_id: int, db : Session ) -> User:
    statement = select(User).where(User.id == user_id)
    user = db.exec(statement).first()
    return user

def get_user_by_email( email: str, db : Session ) -> User:
    statement = select(User).where(User.email == email)
    user = db.exec(statement).first()
    return user

