from typing import Optional

from pydantic import BaseModel


class ListCreateRequest(BaseModel):
    name: str
    description: Optional[str]

class ListResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    board_id: int

class ListUpdateRequest(BaseModel):
    name: Optional[str]
    description: Optional[str]

