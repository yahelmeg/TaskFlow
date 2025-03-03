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
from backend.models.role import RolesEnum
from backend.schemas.authentication import TokenData
from backend.schemas.board import BoardResponse, BoardUserResponse, BoardCreateRequest, BoardUpdateRequest
from backend.utils.board_utils import get_board_by_id, check_if_user_in_board, get_users_in_boards, get_user_board_link
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
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

        new_board = Board(name=board_info.name, description=board_info.description, owner_id=active_user.id)
        self.db.add(new_board)

        self.db.flush()

        role = get_role_by_name(role_name="owner",db=self.db)
        user_board_link =UserBoardLink(user_id=active_user.id,board_id=new_board.id,role_id=role.id)
        self.db.add(user_board_link)

        self.db.commit()
        self.db.refresh(new_board)

        return BoardResponse.model_validate(new_board.model_dump())

    def get_board_users(self, board_id: int) -> List[BoardUserResponse]:

        board = get_board_by_id(board_id=board_id,db=self.db)
        if not board:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Board does not exist")

        users_in_board = get_users_in_boards(board_id=board_id, db=self.db)
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

    def update_board(self,board_id: int,  board_update: BoardUpdateRequest) -> BoardResponse:
        board = get_board_by_id(board_id=board_id,db=self.db)
        if not board:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board does not exist")

        update_data = board_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(board, key, value)

        self.db.commit()
        self.db.refresh(board)

        return BoardResponse.model_validate(board.model_dump())

    def delete_board(self,board_id: int):
        #todo handle cascade deleting, board and tasks in the board should get deleted
        board = get_board_by_id(board_id=board_id,db=self.db)
        if not board:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board does not exist")

        self.db.delete(board)
        self.db.commit()
        return None

    def invite_user_to_board(self, board_id: int, user_id: int,
                             active_user: TokenData = Depends(get_current_user)):
        board = get_board_by_id(board_id=board_id, db=self.db)
        if not board:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board does not exist")
        user = get_user_by_id(user_id=user_id, db=self.db)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
        existing_invitation = get_pending_board_invitation_of_user(user_id=user_id,
                                                                   board_id=board_id, db=self.db)
        if existing_invitation:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already has a pending invitation to this board"
            )
        if check_if_user_in_board(user_id=user_id, board_id=board_id, db=self.db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already in this board"
            )

        new_invitation = Invitation(
                status=InvitationStatus.PENDING,
                board_id=board_id,
                invited_user_id= user_id,
                inviter_user_id= active_user.id
        )
        self.db.add(new_invitation)
        self.db.commit()
        self.db.refresh(new_invitation)

        return {"message": "Invitation sent successfully"}

    def update_user_board_role(self, board_id: int, user_id: int, role_name: str):
        board = get_board_by_id(board_id=board_id, db=self.db)
        if not board:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board does not exist")
        user_board_link = get_user_board_link(board_id=board_id, user_id=user_id, db=self.db)
        if not user_board_link:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User is not a member of this board"
            )
        role = get_role_by_name(role_name=role_name, db=self.db)
        if not role:
            if not role:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Role {role_name} does not exist"
                )
        if role_name == RolesEnum.OWNER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot change user role to owner"
            )
        user_board_link.role_id =  role.id
        self.db.commit()

        return {"message": f"User role updated to {role_name} successfully"}


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

@board_router.post("/{board_id}/invite/{user_id}", status_code=status.HTTP_200_OK)
def invite_user_to_board(board_id: int, user_id: int,
                         controller: BoardController = Depends(get_board_controller),
                         active_user : TokenData = Depends(get_current_user),
                         _: None = Depends(require_board_role(["owner"]))):
    return controller.invite_user_to_board(board_id=board_id,user_id=user_id, active_user=active_user)

@board_router.patch("/{board_id}/role/{user_id}",status_code = status.HTTP_200_OK)
def update_user_board_role(board_id:int,
                           user_id:int,
                           role_name:str,
                           controller: BoardController = Depends(get_board_controller),
                           _: TokenData = Depends(get_current_user),
                           __: None = Depends(require_board_role(["owner"]))):
    return controller.update_user_board_role(board_id=board_id,user_id=user_id,role_name=role_name)








