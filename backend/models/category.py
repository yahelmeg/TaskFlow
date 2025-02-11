from sqlmodel import SQLModel, Field
from typing import Optional

class TaskCategory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None