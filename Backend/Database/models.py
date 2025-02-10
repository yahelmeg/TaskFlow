from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, UTC
from enum import Enum
from db_utils import utc_now


# Link Tables
class UserRoleLink(SQLModel, table=True):
    user_id: int = Field(default=None, foreign_key="user.id", primary_key=True)
    role_id: int = Field(default=None, foreign_key="role.id", primary_key=True)

class UserTeamLink(SQLModel, table=True):
    user_id: int = Field(default=None, foreign_key="user.id", primary_key=True)
    team_id: int = Field(default=None, foreign_key="team.id", primary_key=True)

class TaskCategoryLink(SQLModel, table=True):
    task_id: int = Field(default=None, foreign_key="task.id", primary_key=True)
    category_id: int = Field(default=None, foreign_key="taskcategory.id", primary_key=True)

class RolePermissionLink(SQLModel, table=True):
    role_id: int = Field(default=None, foreign_key="role.id", primary_key=True)
    permission_id: int = Field(default=None, foreign_key="permission.id", primary_key=True)


# Classes
class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    # Relationship
    users: List["User"] = Relationship(back_populates="roles", link_model=UserRoleLink)
    permissions: List["Permission"] = Relationship(back_populates="roles", link_model=RolePermissionLink)

class Permission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str  # e.g., "create_task", "delete_task"
    description: Optional[str] = None

    # Relationship
    roles: List[Role] = Relationship(back_populates="permissions", link_model=RolePermissionLink)

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    created_at: datetime = Field(default_factory=utc_now())

    # Relationships
    roles: List[Role] = Relationship(back_populates="users", link_model=UserRoleLink)
    tasks_received: List["Task"] = Relationship(back_populates="assignee")
    tasks_created: List["Task"] = Relationship(back_populates="task_creator")
    teams: List["Team"] = Relationship(back_populates="members", link_model=UserTeamLink)
    user_activities: List["TaskActivity"] = Relationship(back_populates="user")

class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    # Relationship
    members: List[User] = Relationship(back_populates="teams", link_model=UserTeamLink)

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
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=utc_now)

    # Foreign Keys
    assigned_to_id: Optional[int] = Field(foreign_key="user.id", index=True)
    created_by_id: Optional[int] = Field(foreign_key="user.id", index=True)

    # Relationships
    assignee: Optional[User] = Relationship(back_populates="tasks_received")
    task_creator: Optional[User] = Relationship(back_populates="tasks_created")
    task_activities: List["TaskActivity"] = Relationship(back_populates="task")
    task_categories: List["TaskCategory"] = Relationship(back_populates="tasks", link_model=TaskCategoryLink)

class TaskActivity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id", index=True)
    user_id: Optional[int] = Field(foreign_key="user.id", index=True)
    description: str
    timestamp: datetime = Field(default_factory=utc_now)

    # Relationships
    task: Optional[Task] = Relationship(back_populates="task_activities")
    user: Optional[User] = Relationship(back_populates="user_activities")

class TaskCategory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None

    # Relationships
    tasks: List[Task] = Relationship(back_populates="task_categories", link_model=TaskCategoryLink)







