from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from backend.authentication.jwt_handler import get_current_user
from backend.dependencies.db_dependencies import get_db
from backend.dependencies.board_dependencies import require_board_role
from backend.utils.task_utils import get_task_by_id


def require_board_role_from_task(required_roles: list[str]):
    def extract_board_id_and_check_role(task_id: int, db: Session = Depends(get_db), active_user = Depends(get_current_user)):
        db_task = get_task_by_id(task_id=task_id, db=db)
        if not db_task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="List not found")

        board_id = db_task.board_id
        return require_board_role(required_roles)(board_id, active_user, db)

    return extract_board_id_and_check_role