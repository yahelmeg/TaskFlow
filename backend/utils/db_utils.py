from sqlmodel import Session, select, SQLModel
from fastapi import Depends
from backend.models.user import User
from backend.dependencies.db_dependencies import get_db


def get_user(email: str, db: Session = Depends(get_db)):
    statement = select(User).where(User.email == email)
    user = db.exec(statement).first()
    return user
