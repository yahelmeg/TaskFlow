from typing import Optional

from pydantic import BaseModel


class BoardUserResponse(BaseModel):
    name: str
    email: str
    role_name: str

class BoardResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    owner_id: int

class BoardCreateRequest(BaseModel):
    name: str
    description: Optional[str]

class BoardUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class InviteRequest(BaseModel):
    board_id: int
    user_id: int
