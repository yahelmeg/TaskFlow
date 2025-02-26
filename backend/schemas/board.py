from pydantic import BaseModel
from typing import Optional

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
    name: str
    description: Optional[str]
