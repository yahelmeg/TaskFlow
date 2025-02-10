from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
import datetime
from .task import Task
from .user import User
from backend.database import utc_now

class TaskActivity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str
    timestamp: datetime = Field(default_factory=utc_now)

    # Foreign Keys
    task_id: int = Field(foreign_key="task.id", index=True)
    user_id: Optional[int] = Field(foreign_key="user.id", index=True)

    # Relationships
    task: Optional[Task] = Relationship(back_populates="task_activities")
    user: Optional[User] = Relationship(back_populates="user_activities")