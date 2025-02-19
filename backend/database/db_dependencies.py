from sqlmodel import Session
from backend.database.database import engine

def get_db():
    with Session(engine) as session:
        yield session