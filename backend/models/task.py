from datetime import datetime
from enum import Enum
from typing import List, Optional

from sqlmodel import SQLModel, Field, Relationship

from backend.models.activity import TaskActivity
from backend.models.board import Board
from backend.models.tag import TaskTag
from backend.models.comment import TaskComment
from backend.models.relationships import TaskTagLink, TaskUserLink
from backend.models.user import User
from backend.utils.time_utils import utc_now


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    REVIEW = "review"
    COMPLETED = "completed"

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = Field(default=None)
    priority: Optional[TaskPriority] = Field(default=None)
    status: TaskStatus= Field(default=TaskStatus.TODO)
    created_at: datetime = Field(default_factory=utc_now)
    due_date: Optional[datetime]

    # Relationships
    creator: Optional["User"] = Relationship(link_model=TaskUserLink)
    task_tags: List["TaskTag"] = Relationship(link_model=TaskTagLink)
    task_activities: List["TaskActivity"] = Relationship()
    task_comments: List["TaskComment"] = Relationship()


