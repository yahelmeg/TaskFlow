from sqlmodel import SQLModel, Field
from datetime import datetime

class BlacklistedToken(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    token: str = Field(index=True, unique=True)
    expires_at: datetime