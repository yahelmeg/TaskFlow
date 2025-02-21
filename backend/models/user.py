from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from backend.database.db_utils import utc_now
from backend.models.relationships import UserRoleLink, UserTeamLink
from backend.models.role import Role
from backend.models.team import Team

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    hashed_password: str
    email: str
    created_at: datetime = Field(default_factory=utc_now)

    roles: List[Role] = Relationship(link_model=UserRoleLink)
    team: Optional[Team] = Relationship(link_model=UserTeamLink)


