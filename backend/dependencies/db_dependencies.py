from sqlmodel import Session

from backend.database.db_config import engine


def get_db():
    with Session(engine) as session:
        yield session