from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from backend.utils.time_utils import utc_now

class TaskActivity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str
    timestamp: datetime = Field(default_factory=utc_now)

    # Foreign key
    user_id: int = Field(default=None, foreign_key="user.id", index=True)
    task_id: int = Field(default=None, foreign_key="task.id", index=True)
