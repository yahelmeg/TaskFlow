from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from backend.utils.time_utils import utc_now

class TaskComment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    created_at: datetime = Field(default_factory=utc_now)
    edited_at: Optional[datetime] = Field(default=None)

    # Foreign key
    user_id: int = Field(default=None, foreign_key="user.id", index=True)
    task_id: int = Field(default=None, foreign_key="task.id", index=True)
