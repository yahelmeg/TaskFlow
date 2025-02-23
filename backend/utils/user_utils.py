from backend.database.db_dependencies import get_db
from fastapi import Depends
from sqlmodel import Session, select
from backend.models.user import User


def username_exists(username:str, db : Session = Depends(get_db)) -> bool:
    statement = select(User).where(User.username == username)
    user = db.exec(statement).first()
    if user:
        return True
    return False

def email_exists(email:str, db : Session = Depends(get_db)) -> bool:
    statement = select(User).where(User.email == email)
    user = db.exec(statement).first()
    if user:
        return True
    return False

def get_user_by_id( user_id: int, db : Session = Depends(get_db)) -> User:
    statement = select(User).where(User.id == user_id)
    user = db.exec(statement).first()
    return user

def get_user_by_username( username: str, db : Session = Depends(get_db)) -> User:
    statement = select(User).where(User.username == username)
    user = db.exec(statement).first()
    return user

def get_user_by_email( email: str, db : Session = Depends(get_db)) -> User:
    statement = select(User).where(User.email == email)
    user = db.exec(statement).first()
    return user

