from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select

from backend.dependencies.auth_dependencies import get_current_user
from backend.dependencies.db_dependencies import get_db
from backend.models.board import Board
from backend.models.relationships import UserBoardLink
from backend.models.user import User
from backend.schemas.authentication import TokenData
from backend.schemas.board import BoardResponse
from backend.schemas.user import UserResponse

me_router = APIRouter(prefix="/me", tags=['Me'])

class MeController:
    def __init__(self, db: Session):
        self.db = db

    def get_my_boards(self, active_user: TokenData = Depends(get_current_user)) -> list[BoardResponse]:
        board_statement = select(Board).join(UserBoardLink).where(UserBoardLink.user_id == active_user.id)
        boards = self.db.exec(board_statement).all()
        return [BoardResponse.model_validate(board.model_dump()) for board in boards]

    def get_my_profile(self, active_user: TokenData = Depends(get_current_user)) -> UserResponse:
        user_statement = select(User).where(User.id == active_user.id)
        user = self.db.exec(user_statement).first()
        return UserResponse.model_validate(user.model_dump())


@me_router.get("/board", response_model=list[BoardResponse], status_code=status.HTTP_200_OK)
def get_user_boards(db: Session = Depends(get_db),
                    active_user: TokenData = Depends(get_current_user)):
    return MeController(db).get_my_boards(active_user=active_user)

@me_router.get("/user", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_my_profile(db: Session = Depends(get_db),
                   active_user: TokenData = Depends(get_current_user)):
    return MeController(db).get_my_profile(active_user=active_user)





