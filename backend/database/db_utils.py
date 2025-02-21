from datetime import datetime, UTC
from sqlmodel import Session, select
from fastapi import Depends
from backend.models.user import User
from db_dependencies import get_db

def utc_now() -> datetime:
    return datetime.now(UTC)

def get_user(username: str, db: Session = Depends(get_db)):
    statement = select(User).where(User.username == username)
    user = db.exec(statement).first()
    return user