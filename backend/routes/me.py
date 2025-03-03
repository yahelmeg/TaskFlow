from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select

from backend.authentication.encryption import hash_password
from backend.dependencies.auth_dependencies import get_current_user
from backend.dependencies.db_dependencies import get_db
from backend.models.board import Board
from backend.models.relationships import UserBoardLink
from backend.models.user import User
from backend.schemas.authentication import TokenData
from backend.schemas.board import BoardResponse
from backend.schemas.user import UserResponse
from backend.schemas.invitation import InvitationResponse
from backend.utils.invitation_utils import get_pending_invitations_for_user, get_past_invitations_for_user
from backend.schemas.user import UserUpdateRequest
from backend.utils.user_utils import get_user_by_id, email_exists

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

    def get_my_pending_invitations(self, active_user: TokenData = Depends(get_current_user)) -> list[InvitationResponse]:

        pending_invitations = get_pending_invitations_for_user(user_id=active_user.id,db=self.db)
        return [InvitationResponse.model_validate(invitation.model_dump()) for invitation in pending_invitations]

    def get_my_past_invitations(self, active_user: TokenData = Depends(get_current_user)) -> list[InvitationResponse]:

        past_invitations = get_past_invitations_for_user(user_id=active_user.id,db=self.db)
        return [InvitationResponse.model_validate(invitation.model_dump()) for invitation in past_invitations]

    def update_my_info(self, user_update: UserUpdateRequest, active_user: TokenData = Depends(get_current_user)) -> UserResponse:
        user = get_user_by_id(user_id=active_user.id, db=self.db)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
        if user_update.email and user_update.email != user.email:
            if email_exists(email=user_update.email, db=self.db):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

        update_data = user_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if key == "password":
                setattr(user, "hashed_password", hash_password(password=key))
            elif hasattr(user, key):
                setattr(user, key, value)

        self.db.commit()
        self.db.refresh(user)
        return UserResponse.model_validate(user.model_dump())


def get_me_controller(db: Session = Depends(get_db)) -> MeController:
    return MeController(db)

@me_router.get("/boards", response_model=list[BoardResponse], status_code=status.HTTP_200_OK)
def get_user_boards(controller: MeController = Depends(get_me_controller),
                    active_user: TokenData = Depends(get_current_user)):
    return controller.get_my_boards(active_user=active_user)

@me_router.patch("/user", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_my_info(user_update: UserUpdateRequest,
                   controller: MeController = Depends(get_me_controller),
                   active_user: TokenData = Depends(get_current_user)):
    return controller.update_my_info( user_update=user_update, active_user=active_user)

@me_router.get("/user", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_my_profile(controller: MeController = Depends(get_me_controller),
                   active_user: TokenData = Depends(get_current_user)):
    return controller.get_my_profile(active_user=active_user)

@me_router.get("/pending-invitations", response_model=list[InvitationResponse], status_code=status.HTTP_200_OK)
def get_my_pending_invitations(controller: MeController = Depends(get_me_controller),
                   active_user: TokenData = Depends(get_current_user)):
    return controller.get_my_pending_invitations(active_user=active_user)

@me_router.get("/past-invitations", response_model=list[InvitationResponse], status_code=status.HTTP_200_OK)
def get_my_past_invitations(controller: MeController = Depends(get_me_controller),
                   active_user: TokenData = Depends(get_current_user)):
    return controller.get_my_past_invitations(active_user=active_user)






