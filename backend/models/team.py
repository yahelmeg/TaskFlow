from sqlmodel import SQLModel, Field, Relationship
from .user import User
from typing import List, Optional
from .user import UserTeamLink

class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    # Relationship
    members: List[User] = Relationship(back_populates="teams", link_model=UserTeamLink)