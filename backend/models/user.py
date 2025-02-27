from datetime import datetime
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship

from backend.models.board import Board
from backend.models.relationships import UserRoleLink, UserBoardLink
from backend.models.role import Role
from backend.utils.time_utils import utc_now


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    hashed_password: str
    email: str
    created_at: datetime = Field(default_factory=utc_now)

    #Relationships
    roles: List[Role] = Relationship(link_model=UserRoleLink)
    board: Optional[Board] = Relationship(link_model=UserBoardLink)


