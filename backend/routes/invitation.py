from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from backend.authentication.jwt_handler import get_current_user
from backend.models.relationships import UserBoardLink
from backend.schemas.authentication import TokenData
from backend.models.invitation import InvitationStatus
from backend.dependencies.db_dependencies import get_db
from backend.utils.invitation_utils import get_invitation_of_user
from backend.utils.role_utils import get_role_by_name
from backend.utils.board_utils import get_user_board_link

invitation_router = APIRouter(prefix="/invitation", tags=['Invitation'])

class InvitationController:
    def __init__(self, db: Session):
        self.db = db

    def accept_invitation(self, invitation_id : int , active_user: TokenData = Depends(get_current_user)) -> dict:

        invitation = get_invitation_of_user(invitation_id=invitation_id, user_id=active_user.id,
                                            db=self.db)
        if not invitation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invitation does not exist")

        if invitation.status != InvitationStatus.PENDING:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invitation is already processed")


        board_user_link = get_user_board_link(board_id=invitation.board_id, user_id=active_user.id,db=self.db)

        if board_user_link:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is already a member of this board")

        role = get_role_by_name(role_name="viewer", db=self.db)
        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role does not exist")

        invitation.status = InvitationStatus.ACCEPTED
        self.db.add(invitation)
        board_user_link = UserBoardLink(board_id=invitation.board_id, user_id=active_user.id, role_id=role.id)
        self.db.add(board_user_link)
        self.db.commit()

        return {"message": "Invitation accepted"}

    def decline_invitation(self, invitation_id: int, active_user: TokenData = Depends(get_current_user)) -> dict:

        invitation = get_invitation_of_user(invitation_id=invitation_id, user_id=active_user.id,
                                            db=self.db)
        if not invitation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invitation does not exist")

        if invitation.status != InvitationStatus.PENDING:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invitation already processed")

        invitation.status = InvitationStatus.DECLINED
        self.db.add(invitation)
        self.db.commit()

        return {"message": "Invitation declined"}

def get_invitation_controller(db: Session = Depends(get_db)) -> InvitationController:
    return InvitationController(db)

@invitation_router.post("/{invitation_id}/accept", status_code=status.HTTP_200_OK)
def accept_invitation(invitation_id: int,
                      active_user: TokenData = Depends(get_current_user),
                      controller: InvitationController = Depends(get_invitation_controller)):
    return controller.accept_invitation(invitation_id=invitation_id,active_user=active_user)

@invitation_router.post("/{invitation_id}/decline", status_code = status.HTTP_200_OK)
def decline_invitation(invitation_id: int,
                       active_user: TokenData = Depends(get_current_user),
                       controller: InvitationController = Depends(get_invitation_controller)):
    return controller.decline_invitation(invitation_id=invitation_id, active_user= active_user)