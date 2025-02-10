from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from .role import Role
from .team import Team
from .task import Task
from .activity import TaskActivity
from .comment import TaskComment
from backend.database.db_utils import utc_now

class UserRoleLink(SQLModel, table=True):
    user_id: int = Field(default=None, foreign_key="user.id", primary_key=True)
    role_id: int = Field(default=None, foreign_key="role.id", primary_key=True)

class UserTeamLink(SQLModel, table=True):
    user_id: int = Field(default=None, foreign_key="user.id", primary_key=True)
    team_id: int = Field(default=None, foreign_key="team.id", primary_key=True)

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    created_at: datetime = Field(default_factory=utc_now)

    # Relationships
    roles: List[Role] = Relationship(back_populates="users", link_model=UserRoleLink)
    tasks_received: List["Task"] = Relationship(back_populates="assignee")
    tasks_created: List["Task"] = Relationship(back_populates="task_creator")
    teams: List["Team"] = Relationship(back_populates="members", link_model=UserTeamLink)
    user_activities: List["TaskActivity"] = Relationship(back_populates="user")
    comments: List["TaskComment"] = Relationship(back_populates="user")