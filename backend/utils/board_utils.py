from sqlmodel import Session, select

from backend.models.board import Board
from backend.models.relationships import UserBoardLink
from backend.models.user import User
from backend.models.role import Role


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

def get_users_in_boards(board_id: int, db:Session):
    users_in_board_statement = (
                select(User, Role)
                .select_from(User)
                .join(UserBoardLink)
                .join(Role)
                .where(UserBoardLink.board_id == board_id)
    )
    users_in_board = db.exec(users_in_board_statement).all()
    return users_in_board

def get_user_board_link(board_id:int, user_id:int, db:Session):
    link_statement = (
                select(UserBoardLink)
                .where(UserBoardLink.board_id == board_id)
                .where(UserBoardLink.user_id == user_id)
    )

    board_user_link = db.exec(link_statement).first()

    return board_user_link



