from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from backend.models.relationships import RolePermissionLink
from backend.models.permission import  Permission

class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    # Relationships
    permissions: List["Permission"] = Relationship(link_model=RolePermissionLink)



