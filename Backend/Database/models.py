from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, UTC


class UserBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

# User inherits from UserBase
class User(UserBase, table=True):
    tasks_assigned: List["Task"] = Relationship(back_populates="assigned_to")

# TaskGiver inherits from UserBase
class TaskGiver(UserBase, table=True):
    tasks_assigned: List["Task"] = Relationship(back_populates="task_giver")

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    assigned_by_id: Optional[int] = Field(foreign_key="taskgiver.id", index=True)
    assigned_to_id: Optional[int] = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    task_giver: Optional["TaskGiver"] = Relationship(back_populates="assigned_tasks")
    assigned_to: Optional[User] = Relationship(back_populates="tasks_assigned")

