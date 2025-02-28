from pydantic import BaseModel

from backend.models.invitation import InvitationStatus
from datetime import datetime

class InvitationResponse(BaseModel):
    id: int
    status: InvitationStatus
    created_at: datetime
    board_id: int
    inviter_user_id: int