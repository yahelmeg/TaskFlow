from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from backend.utils.time_utils import utc_now


class TaskList(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=utc_now)

    # foreign key
    board_id: int = Field(default=None, foreign_key="board.id", index=True)
