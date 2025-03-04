from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from backend.authentication.jwt_handler import get_current_user
from backend.dependencies.db_dependencies import get_db
from backend.models.task import Task

from backend.schemas.authentication import TokenData
from backend.schemas.task import TaskCreateRequest, TaskResponse, TaskUpdateRequest
from backend.utils.board_utils import get_board_by_id
from backend.utils.task_utils import get_task_by_id, get_tasks_of_list, get_tasks_of_board
from backend.utils.list_utils import get_task_list_by_id
from backend.dependencies.list_dependencies import require_board_role_from_list
from backend.dependencies.task_dependency import require_board_role_from_task
from backend.dependencies.board_dependencies import any_roles, edit_roles, require_board_role

task_router = APIRouter(tags=['Task'])

class TaskController:
    def __init__(self, db: Session):
        self.db = db

    def create_task(self, task_list_id: int, task_info: TaskCreateRequest,
                    active_user: TokenData = Depends(get_current_user)) -> TaskResponse:
        task_list = get_task_list_by_id(task_list_id=task_list_id, db=self.db)
        if not task_list:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="List does not exist")
        new_task = Task(
            title=task_info.title,
            description=task_info.description,
            priority=task_info.priority,
            status=task_info.status,
            due_date=task_info.due_date,
            list_id=task_list_id,
            creator_id=active_user.id,
            board_id = task_list.board_id
        )

        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)

        return TaskResponse.model_validate(new_task.model_dump())

    def delete_task(self, task_id: int) -> None:
        db_task = get_task_by_id(task_id=task_id, db=self.db)
        if not db_task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task does not exist")

        self.db.delete(db_task)
        self.db.commit()

        return None

    def get_task(self, task_id: int) -> TaskResponse:
        db_task = get_task_by_id(task_id=task_id, db=self.db)
        if not db_task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task does not exist")

        return TaskResponse.model_validate(db_task.model_dump())

    def update_task(self,task_id: int, task_update: TaskUpdateRequest) -> TaskResponse:
        db_task = get_task_by_id(task_id=task_id, db=self.db)
        if not db_task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task does not exist")

        update_data = task_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)

        self.db.commit()
        self.db.refresh(db_task)

        return TaskResponse.model_validate(db_task.model_dump())

    def get_list_tasks(self, list_id: int) ->  List[TaskResponse]:
        task_list = get_task_list_by_id(task_list_id=list_id, db=self.db)
        if not task_list:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task list does not found")

        tasks = get_tasks_of_list(list_id=list_id, db=self.db)
        return [TaskResponse.model_validate(task.model_dump()) for task in tasks]

    def get_board_tasks(self, board_id: int) -> List[TaskResponse]:
        board = get_board_by_id(board_id=board_id, db=self.db)
        if not board:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board does not exist")
        tasks = get_tasks_of_board(board_id=board_id, db=self.db)
        return [TaskResponse.model_validate(task.model_dump()) for task in tasks]



def get_task_controller(db: Session = Depends(get_db)) -> TaskController:
    return TaskController(db)

@task_router.get("/task/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def get_task(task_id: int,
             controller: TaskController = Depends(get_task_controller),
             _: TokenData = Depends(get_current_user),
             __: None = Depends(require_board_role_from_task(any_roles()))):
    return controller.get_task(task_id=task_id)

@task_router.delete("/task/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int,
                controller: TaskController = Depends(get_task_controller),
                _: TokenData = Depends(get_current_user),
                __: None = Depends(require_board_role_from_task(edit_roles()))):
    return controller.delete_task(task_id=task_id)

@task_router.patch("/task/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def update_task(task_id: int,
                task_update: TaskUpdateRequest,
                controller: TaskController = Depends(get_task_controller),
                 _: TokenData = Depends(get_current_user),
                __: None = Depends(require_board_role_from_task(edit_roles()))):
    return controller.update_task(task_id=task_id, task_update=task_update)

@task_router.post("/list/{list_id}/task", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(list_id: int,
                task_info: TaskCreateRequest,
                controller: TaskController = Depends(get_task_controller),
                active_user: TokenData = Depends(get_current_user),
                __: None = Depends(require_board_role_from_list(edit_roles()))):
    return controller.create_task(task_list_id=list_id, task_info=task_info, active_user=active_user)

@task_router.get("/list/{list_id}/task", response_model=List[TaskResponse], status_code=status.HTTP_200_OK)
def get_list_tasks(list_id: int,
                   controller: TaskController = Depends(get_task_controller),
                   _: TokenData = Depends(get_current_user),
                   __: None = Depends(require_board_role_from_list(any_roles()))):
    return controller.get_list_tasks(list_id=list_id)

@task_router.get("/board/{board_id}/task", response_model=List[TaskResponse], status_code=status.HTTP_200_OK)
def get_board_tasks(board_id: int,
                    controller: TaskController = Depends(get_task_controller),
                    _: TokenData = Depends(get_current_user),
                    __: None = Depends(require_board_role(any_roles()))):
    return controller.get_board_tasks(board_id=board_id)







