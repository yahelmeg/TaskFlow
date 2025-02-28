from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

from backend.utils.time_utils import utc_now
from backend.models.user import User

class InvitationStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"

class Invitation(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    status: InvitationStatus = Field(default=InvitationStatus.PENDING)
    created_at: datetime = Field(default_factory=utc_now)

    board_id: int = Field(foreign_key="board.id")
    invited_user_id: int = Field(foreign_key="user.id")
    inviter_user_id: int = Field(foreign_key="user.id")

    invited_user: Optional[User] = Relationship(sa_relationship_kwargs={"foreign_keys": "Invitation.invited_user_id"})
    inviter_user: Optional[User] = Relationship(sa_relationship_kwargs={"foreign_keys": "Invitation.inviter_user_id"})
