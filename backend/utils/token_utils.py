from sqlmodel import Session, select
from datetime import datetime, UTC

from backend.authentication.jwt_handler import verify_token
from backend.models.blacklistedtoken import BlacklistedToken

def blacklist_refresh_token(token: str, expires_at: datetime, db: Session):
    db_token = BlacklistedToken(token=token, expires_at=expires_at)
    db.add(db_token)
    db.commit()

def check_blacklisted(token:str, db: Session):
    existing_blacklist = db.exec(
        select(BlacklistedToken).where(BlacklistedToken.token == token)
    ).first()

    if existing_blacklist:
        return True
    return False
