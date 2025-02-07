from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, UTC


# Link Tables
class UserRoleLink(SQLModel, table=True):
    user_id: int = Field(default=None, foreign_key="user.id", primary_key=True)
    role_id: int = Field(default=None, foreign_key="role.id", primary_key=True)

# Classes
class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    # Relationship
    users: List["User"] = Relationship(back_populates="roles", link_model=UserRoleLink) # Many-to-Many

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # Relationships
    roles: List[Role] = Relationship(back_populates="users", link_model=UserRoleLink) # Many-to-Many
    tasks_received: List["Task"] = Relationship(back_populates="assigned_to") # One-to-Many
    tasks_created: List["Task"] = Relationship(back_populates="task_giver") # One-to-Many


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # Foreign Keys
    assigned_to_id: Optional[int] = Field(foreign_key="user.id", index=True)
    created_by_id: Optional[int] = Field(foreign_key="user.id", index=True)

    # Relationships
    assigned_to: Optional[User] = Relationship(back_populates="tasks_received") # One-to-Many
    task_giver: Optional[User] = Relationship(back_populates="tasks_created") # One-to-Many

