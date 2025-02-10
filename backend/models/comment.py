from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
import datetime
from .task import Task
from .user import User
from backend.database.db_utils import utc_now

class TaskComment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    created_at: datetime = Field(default_factory=utc_now)
    edited_at: Optional[datetime] = Field(default=None)

    # Foreign keys
    task_id: int = Field(default=None, foreign_key="task.id", index=True)
    user_id: int = Field(default=None, foreign_key="user.id", index=True)

    # Relationships
    task: Optional[Task] = Relationship(back_populates="comments")
    user: Optional[User] = Relationship(back_populates="comments")