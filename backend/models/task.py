from datetime import datetime
from enum import Enum
from typing import List, Optional

from sqlmodel import SQLModel, Field, Relationship

from backend.models.activity import TaskActivity
from backend.models.board import Board
from backend.models.category import TaskCategory
from backend.models.comment import TaskComment
from backend.models.relationships import TaskCategoryLink, TaskBoardLink, TaskUserLink
from backend.models.user import User
from backend.utils.time_utils import utc_now


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = Field(default=None)
    priority: Optional[TaskPriority] = Field(default=None)
    completed: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default_factory=utc_now)

    # Relationships
    board: Optional["Board"] = Relationship(link_model=TaskBoardLink)
    creator: Optional["User"] = Relationship(link_model=TaskUserLink)

    task_categories: List["TaskCategory"] = Relationship(link_model=TaskCategoryLink)
    task_activities: List["TaskActivity"] = Relationship()
    task_comments: List["TaskComment"] = Relationship()


