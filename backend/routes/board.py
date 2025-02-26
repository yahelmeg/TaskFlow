from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel import Session, select
from backend.authentication.jwt_handler import get_current_user
from backend.dependencies.auth_dependencies import require_role
from backend.models.board import Board
from backend.utils.user_utils import get_user_by_id
from backend.models.user import User
from backend.models.relationships import UserBoardLink
from backend.schemas.board import BoardResponse, BoardUserResponse, BoardCreateRequest, BoardUpdateRequest
from backend.utils.db_utils import db_add_and_refresh
from backend.schemas.authentication import TokenData
from backend.utils.board_utils import get_board_by_id
from backend.utils.role_utils import get_role_by_name , get_role_by_id
from backend.dependencies.db_dependencies import get_db
from backend.dependencies.board_dependencies import require_board_role


board_router = APIRouter(prefix="/board", tags=['Board'])

class BoardController:
    def __init__(self, db: Session):
        self.db = db

    def create_board(self, board_info: BoardCreateRequest, active_user: TokenData = Depends(get_current_user)) -> BoardResponse:

        user = get_user_by_id(user_id=active_user.id, db=self.db)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        new_board = db_add_and_refresh(
            db=self.db,
            obj=Board(name=board_info.name, description=board_info.description, owner_id=active_user.id)
        )
        role = get_role_by_name(role_name="owner",db=self.db)
        db_add_and_refresh(
            db=self.db,
            obj=UserBoardLink(user_id=active_user.id,board_id=new_board.id,role_id=role.id)
        )
        return BoardResponse.model_validate(new_board.model_dump())

    def get_board_users(self, board_id: int) -> List[BoardUserResponse]:

        board = get_board_by_id(board_id=board_id,db=self.db)
        if not board:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Board not found")
        users_in_board_statement = select(User,UserBoardLink.role_id).join(UserBoardLink).where(UserBoardLink.board_id == board.id)
        users_in_board = self.db.exec(users_in_board_statement).all()
        #todo : improve this by querying role names once instead of doing it for every user
        user_responses = [
            BoardUserResponse(
                name = user.name,
                email = user.email,
                role_name = (get_role_by_id(role_id=role_id,db=self.db)).name
            )
            for user, role_id in users_in_board
        ]
        return user_responses

    def get_boards(self) -> List[BoardResponse]:
        boards = self.db.exec(select(Board)).all()
        return [BoardResponse.model_validate(board.model_dump()) for board in boards]

    def update_board(self,board_id: int,  board_info: BoardUpdateRequest) -> BoardResponse:
        board = get_board_by_id(board_id=board_id,db=self.db)
        if not board:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")
        if board_info.name:
            board.name = board_info.name
        if board_info.description:
            board.description = board_info.description

        self.db.commit()
        self.db.refresh(board)

        return BoardResponse.model_validate(board.model_dump())

    def delete_board(self,board_id: int):
        #todo handle cascade deleting
        board = get_board_by_id(board_id=board_id,db=self.db)
        if not board:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")

        self.db.delete(board)
        self.db.commit()

        return None

    def add_user_to_board(self, board_id: int):
        #todo check that the request comes from board owner
        board = get_board_by_id(board_id=board_id, db=self.db)
        if not board:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")

        #todo finish this
        return

@board_router.post("/create", response_model=BoardResponse, status_code=status.HTTP_201_CREATED)
def create_board(board_info: BoardCreateRequest,
                 db: Session = Depends(get_db),
                active_user: TokenData = Depends(get_current_user)):
    return BoardController(db).create_board(board_info=board_info,active_user=active_user)

@board_router.get("/{board_id}/users", response_model=List[BoardUserResponse], status_code=status.HTTP_200_OK)
def get_board_users(board_id: int,
                    db: Session = Depends(get_db),
                    _: TokenData = Depends(get_current_user),
                    __: None = Depends(require_board_role(["owner","contributor","viewer"]))):
    return BoardController(db).get_board_users(board_id=board_id)

@board_router.get("/", response_model=List[BoardResponse], status_code=status.HTTP_200_OK)
def get_boards(db: Session = Depends(get_db),
               _: TokenData = Depends(get_current_user),
               __: TokenData = Depends(require_role(["admin"]))):
    return BoardController(db).get_boards()

@board_router.patch("/update/{{board_id}}", response_model=BoardResponse, status_code=status.HTTP_200_OK)
def update_board(board_id : int,
                 board_info: BoardUpdateRequest,
                 db: Session = Depends(get_db),
                 _: TokenData = Depends(get_current_user),
                 __: None = Depends(require_board_role(["owner"]))):
    return BoardController(db).update_board(board_id=board_id, board_info=board_info)

@board_router.delete("/delete/{{board_id}}", status_code = status.HTTP_204_NO_CONTENT)
def delete_board(board_id: int,
                 db: Session = Depends(get_db),
                 _: TokenData = Depends(get_current_user),
                 __: None = Depends(require_board_role(["owner"]))):
    return BoardController(db).delete_board(board_id=board_id)
