from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from backend.models.task import TaskPriority, TaskStatus


class TaskCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[TaskPriority] = TaskPriority.NONE
    status: TaskStatus = TaskStatus.TODO
    due_date: Optional[datetime] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: Optional[TaskPriority]
    status: TaskStatus
    due_date: Optional[datetime]
    list_id: int
    creator_id: int
    board_id: int

class TaskUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[datetime] = None



