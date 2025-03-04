from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select

from backend.authentication.jwt_handler import get_current_user
from backend.dependencies.db_dependencies import get_db
from backend.models.relationships import UserBoardLink
from backend.schemas.authentication import TokenData
from backend.utils.board_utils import get_board_by_id
from backend.utils.role_utils import get_role_by_name


def require_board_role(required_roles: list[str]):
    def role_checker(board_id: int, active_user: TokenData = Depends(get_current_user), db: Session = Depends(get_db)):
        db_board = get_board_by_id(board_id=board_id, db=db)
        if not db_board:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board does not exist")
        role_ids = []
        for role in required_roles:
            db_role = get_role_by_name(role_name=role, db=db)
            if not db_role:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role {role} does not exist")
            role_ids.append(db_role.id)
        statement = select(UserBoardLink).where(
            (UserBoardLink.user_id == active_user.id) & (UserBoardLink.board_id == board_id)
        )
        user_board_link = db.exec(statement).first()
        if not user_board_link:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not assigned to this board")
        if user_board_link.role_id not in role_ids:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User does not have the required role")

        return active_user

    return role_checker
