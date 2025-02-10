from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
import datetime
from enum import Enum
from .user import User
from .comment import TaskComment
from .activity import TaskActivity
from backend.database.db_utils import utc_now

class TaskCategoryLink(SQLModel, table=True):
    task_id: int = Field(default=None, foreign_key="task.id", primary_key=True)
    category_id: int = Field(default=None, foreign_key="taskcategory.id", primary_key=True)

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
    assigned_to_id: Optional[int] = Field(foreign_key="user.id", index=True)
    created_by_id: Optional[int] = Field(foreign_key="user.id", index=True)

    # Relationships
    assignee: Optional[User] = Relationship(back_populates="tasks_received")
    task_creator: Optional[User] = Relationship(back_populates="tasks_created")
    task_activities: List["TaskActivity"] = Relationship(back_populates="task")
    task_categories: List["TaskCategory"] = Relationship(back_populates="tasks", link_model=TaskCategoryLink)
    comments: List["TaskComment"] = Relationship(back_populates="task")

class TaskCategory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None

    # Relationships
    tasks: List[Task] = Relationship(back_populates="task_categories", link_model=TaskCategoryLink)