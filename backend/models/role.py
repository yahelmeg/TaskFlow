from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from .user import User, UserRoleLink


class RolePermissionLink(SQLModel, table=True):
    role_id: int = Field(default=None, foreign_key="role.id", primary_key=True)
    permission_id: int = Field(default=None, foreign_key="permission.id", primary_key=True)

class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    # Relationship
    users: List["User"] = Relationship(back_populates="roles", link_model=UserRoleLink)
    permissions: List["Permission"] = Relationship(back_populates="roles", link_model=RolePermissionLink)

class Permission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str  # e.g., "create_task", "delete_task"
    description: Optional[str] = None

    # Relationship
    roles: List[Role] = Relationship(back_populates="permissions", link_model=RolePermissionLink)