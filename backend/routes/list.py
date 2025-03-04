from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from backend.authentication.jwt_handler import get_current_user
from backend.dependencies.board_dependencies import require_board_role
from backend.dependencies.db_dependencies import get_db
from backend.models.task_list import TaskList

from backend.schemas.authentication import TokenData
from backend.schemas.list import ListCreateRequest, ListUpdateRequest, ListResponse
from backend.utils.board_utils import get_board_by_id
from backend.utils.list_utils import get_task_list_by_id, get_lists_of_board


list_router = APIRouter(prefix="/board", tags=['List'])

class ListController:
    def __init__(self, db: Session):
        self.db = db

    def create_list(self, board_id: int, list_info: ListCreateRequest) ->ListResponse:

        db_board = get_board_by_id(board_id=board_id,db=self.db)
        if not db_board:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board does not exist")
        new_list = TaskList(name=list_info.name, description=list_info.description, board_id=board_id)

        self.db.add(new_list)
        self.db.commit()
        self.db.refresh(new_list)

        return ListResponse.model_validate(new_list.model_dump())

    def update_list(self, list_id: int, list_update: ListUpdateRequest) -> ListResponse:

        db_list = get_task_list_by_id(task_list_id=list_id, db=self.db )
        if not db_list:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="List does not exist")

        update_data = list_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_list, key, value)

        self.db.commit()
        self.db.refresh(db_list)

        return ListResponse.model_validate(db_list.model_dump())

    def delete_list(self, list_id: int) -> None:
        db_list = get_task_list_by_id(task_list_id=list_id, db=self.db )
        if not db_list:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="List does not exist")

        self.db.delete(db_list)
        self.db.commit()

        return None

    def get_list(self, list_id: int) -> ListResponse:
        db_list = get_task_list_by_id(task_list_id=list_id, db=self.db )
        if not db_list:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="List does not exist")

        return ListResponse.model_validate(db_list.model_dump())

    def get_board_lists(self, board_id: int) -> List[ListResponse]:
        db_board = get_board_by_id(board_id=board_id, db=self.db)
        if not db_board:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board does not exist")
        lists = get_lists_of_board(board_id, self.db)
        return [ListResponse.model_validate(db_list.model_dump()) for db_list in lists]


def get_list_controller(db: Session = Depends(get_db)) -> ListController:
    return ListController(db)

@list_router.post("/{board_id}/list", response_model=ListResponse, status_code=status.HTTP_201_CREATED)
def create_list(board_id: int,
                list_info: ListCreateRequest,
                controller: ListController = Depends(get_list_controller),
                _: TokenData = Depends(get_current_user),
                __: None = Depends(require_board_role(["owner", "contributor"]))):
    return controller.create_list(board_id=board_id, list_info=list_info)

@list_router.patch("/{board_id}/list/{list_id}", response_model=ListResponse, status_code=status.HTTP_200_OK)
def update_list(list_id: int,
                list_update: ListUpdateRequest,
                controller: ListController = Depends(get_list_controller),
                _: TokenData = Depends(get_current_user),
                __: None = Depends(require_board_role(["owner", "contributor"]))):
    return controller.update_list(list_id=list_id, list_update=list_update)

@list_router.delete("/{board_id}/list/{list_id}",  status_code=status.HTTP_204_NO_CONTENT)
def delete_list(list_id: int,
                controller: ListController = Depends(get_list_controller),
                _: TokenData = Depends(get_current_user),
                __: None = Depends(require_board_role(["owner", "contributor"]))):
    return controller.delete_list(list_id=list_id)

@list_router.get("/{board_id}/list/{list_id}", response_model=ListResponse, status_code=status.HTTP_200_OK)
def get_list(list_id: int,
            controller: ListController = Depends(get_list_controller),
            _: TokenData = Depends(get_current_user),
            __: None = Depends(require_board_role(["owner", "contributor", "viewer"]))):
    return controller.get_list(list_id=list_id)

@list_router.get("/{board_id}/list", response_model=List[ListResponse], status_code=status.HTTP_200_OK)
def get_board_lists(board_id: int,
                controller: ListController = Depends(get_list_controller),
                _: TokenData = Depends(get_current_user),
                __: None = Depends(require_board_role(["owner", "contributor", "viewer"]))):
    return controller.get_board_lists(board_id=board_id)
