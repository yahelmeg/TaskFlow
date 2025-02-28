from sqlmodel import Session, select

from backend.models.invitation import Invitation, InvitationStatus

def get_invitation_of_user(invitation_id: int, user_id: int, db : Session) -> Invitation:
    invitation_statement = (
        select(Invitation)
        .where(Invitation.id == invitation_id)
        .where(Invitation.invited_user_id == user_id)
    )
    invitation = db.exec(invitation_statement).first()
    return invitation

def get_pending_invitations_for_user(user_id: int, db: Session) -> list[Invitation]:
    invitation_statement = (
        select(Invitation)
        .where(Invitation.invited_user_id == user_id)
        .where(Invitation.status == InvitationStatus.PENDING)
    )
    pending_invitations =db.exec(invitation_statement).all()
    return pending_invitations

def get_past_invitations_for_user(user_id: int, db: Session) -> list[Invitation]:
    invitation_statement = (
        select(Invitation)
        .where(Invitation.invited_user_id == user_id)
        .where(Invitation.status != InvitationStatus.PENDING)
    )
    past_invitations =db.exec(invitation_statement).all()
    return past_invitations

def get_pending_board_invitation_of_user(board_id: int, user_id: int, db : Session) -> Invitation:
    invitation_statement = (
        select(Invitation)
        .where(Invitation.board_id == board_id)
        .where(Invitation.invited_user_id == user_id)
        .where(Invitation.status == InvitationStatus.PENDING)
    )
    invitation = db.exec(invitation_statement).first()
    return invitation