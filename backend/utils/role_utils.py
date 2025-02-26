from sqlmodel import Session, select
from backend.models.role import Role

def get_role_by_name(role_name: str , db: Session):
    role_statement = select(Role).where(Role.name == role_name)
    role = db.exec(role_statement).first()
    return role

def get_role_by_id(role_id: int, db: Session):
    role_statement = select(Role).where(Role.id == role_id)
    role = db.exec(role_statement).first()
    return role