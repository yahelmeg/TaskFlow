from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from backend.authentication.jwt_handler import get_current_user
from backend.dependencies.auth_dependencies import require_role
from backend.dependencies.board_dependencies import require_board_role
from backend.dependencies.db_dependencies import get_db
from backend.models.board import Board
from backend.models.invitation import Invitation, InvitationStatus
from backend.models.relationships import UserBoardLink
from backend.models.role import Role
from backend.models.user import User
from backend.schemas.authentication import TokenData
from backend.schemas.board import BoardResponse, BoardUserResponse, BoardCreateRequest, BoardUpdateRequest, InviteRequest
from backend.utils.board_utils import get_board_by_id, check_if_user_in_board
from backend.utils.db_utils import db_add_and_refresh
from backend.utils.role_utils import get_role_by_name
from backend.utils.user_utils import get_user_by_id
from backend.utils.invitation_utils import get_pending_board_invitation_of_user

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
        users_in_board_statement = (
            select(User, Role)
            .select_from(User)
            .join(UserBoardLink)
            .join(Role)
            .where(UserBoardLink.board_id == board.id)
        )
        users_in_board = self.db.exec(users_in_board_statement).all()
        user_responses = [
            BoardUserResponse(
                name = user.name,
                email = user.email,
                role_name = role.name
            )
            for user, role in users_in_board
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
        #todo handle cascade deleting, board and tasks in the board should get deleted
        board = get_board_by_id(board_id=board_id,db=self.db)
        if not board:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")

        self.db.delete(board)
        self.db.commit()
        return None

    def invite_user_to_board(self, invite_info: InviteRequest,
                             active_user: TokenData = Depends(get_current_user)):
        #todo check that the request comes from board owner
        board = get_board_by_id(board_id=invite_info.board_id, db=self.db)
        if not board:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")
        user = get_user_by_id(user_id=invite_info.user_id, db=self.db)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        existing_invitation = get_pending_board_invitation_of_user(user_id=invite_info.user_id,
                                                                   board_id=invite_info.board_id, db=self.db)
        if existing_invitation:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already has a pending invitation to this board"
            )
        if check_if_user_in_board(user_id=invite_info.user_id, board_id=invite_info.board_id, db=self.db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already in this board"
            )

        db_add_and_refresh(
            db=self.db,
            obj=Invitation(
                status=InvitationStatus.PENDING,
                board_id=board_id,
                invited_user_id= user_id,
                inviter_user_id= active_user.id
            )
        )

        return {"message": "Invitation sent successfully"}

def get_board_controller(db: Session = Depends(get_db)) ->BoardController:
    return BoardController(db)

@board_router.post("/create", response_model=BoardResponse, status_code=status.HTTP_201_CREATED)
def create_board(board_info: BoardCreateRequest,
                 controller: BoardController = Depends(get_board_controller),
                active_user: TokenData = Depends(get_current_user)):
    return controller.create_board(board_info=board_info,active_user=active_user)

@board_router.get("/{board_id}/users", response_model=List[BoardUserResponse], status_code=status.HTTP_200_OK)
def get_board_users(board_id: int,
                    controller: BoardController = Depends(get_board_controller),
                    _: TokenData = Depends(get_current_user),
                    __: None = Depends(require_board_role(["owner","contributor","viewer"]))):
    return controller.get_board_users(board_id=board_id)

@board_router.get("/", response_model=List[BoardResponse], status_code=status.HTTP_200_OK)
def get_boards(controller: BoardController = Depends(get_board_controller),
               _: TokenData = Depends(get_current_user),
               __: TokenData = Depends(require_role(["admin"]))):
    return controller.get_boards()

@board_router.patch("/update/{board_id}", response_model=BoardResponse, status_code=status.HTTP_200_OK)
def update_board(board_id : int,
                 board_info: BoardUpdateRequest,
                 controller: BoardController = Depends(get_board_controller),
                 _: TokenData = Depends(get_current_user),
                 __: None = Depends(require_board_role(["owner"]))):
    return controller.update_board(board_id=board_id, board_info=board_info)

@board_router.delete("/delete/{board_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_board(board_id: int,
                 controller: BoardController = Depends(get_board_controller),
                 _: TokenData = Depends(get_current_user),
                 __: None = Depends(require_board_role(["owner"]))):
    return controller.delete_board(board_id=board_id)

@board_router.post("/{board_id}/invite", status_code=status.HTTP_200_OK)
def invite_user_to_board(invite_info: InviteRequest,
                         controller: BoardController = Depends(get_board_controller),
                         active_user : TokenData = Depends(get_current_user),
                         _: None = Depends(require_board_role(["owner"]))):
    return controller.invite_user_to_board(invite_info=invite_info, active_user=active_user)







