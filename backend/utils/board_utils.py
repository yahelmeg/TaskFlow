from sqlmodel import Session, select

from backend.models.board import Board
from backend.models.relationships import UserBoardLink


def get_board_by_id( board_id: int, db : Session ) -> Board:
    statement = select(Board).where(Board.id == board_id)
    board = db.exec(statement).first()
    return board

def check_if_user_in_board(board_id: int, user_id: int, db: Session) -> bool:
    statement = (select(UserBoardLink)
                .where(UserBoardLink.user_id == user_id)
                .where(UserBoardLink.board_id == board_id)
    )
    user_board_link = db.exec(statement).first()
    if user_board_link:
        return True
    return False



