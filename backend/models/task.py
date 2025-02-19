from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime
from enum import Enum
from backend.database.db_utils import utc_now
from backend.models.relationships import TaskCategoryLink

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

    # Foreign Keys
    assignee_id: Optional[int] = Field(foreign_key="user.id", index=True)
    created_by_id: Optional[int] = Field(foreign_key="user.id", index=True)

    # Relationships
    assignee: Optional["User"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "Task.assigned_to_id"}
    )
    created_by: Optional["User"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "Task.created_by_id"}
    )
    task_categories: List["TaskCategory"] = Relationship(link_model=TaskCategoryLink)
    task_activities: List["TaskActivity"] = Relationship()
    task_comments: List["TaskComment"] = Relationship()


