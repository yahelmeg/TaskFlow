from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship
from backend.models.list import TaskList


class Board(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    owner_id: int

    # Relationships
    task_lists: List["TaskList"] = Relationship()
