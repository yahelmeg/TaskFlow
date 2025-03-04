from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from backend.authentication.jwt_handler import get_current_user
from backend.dependencies.db_dependencies import get_db
from backend.utils.list_utils import get_task_list_by_id
from backend.dependencies.board_dependencies import require_board_role

def require_board_role_from_list(required_roles: list[str]):
    def extract_board_id_and_check_role(list_id: int, db: Session = Depends(get_db), active_user = Depends(get_current_user)):
        db_list = get_task_list_by_id(task_list_id=list_id, db=db)
        if not db_list:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="List not found")

        board_id = db_list.board_id
        return require_board_role(required_roles)(board_id, active_user, db)

    return extract_board_id_and_check_role