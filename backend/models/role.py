from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field


class RolesEnum(str, Enum):
    ADMIN = "admin"
    OWNER = "owner"
    CONTRIBUTOR = "contributor"
    VIEWER = "viewer"

class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
