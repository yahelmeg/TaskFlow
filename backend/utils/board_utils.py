from sqlmodel import Session, select
from backend.models.board import Board

def get_board_by_id( board_id: int, db : Session ) -> Board:
    statement = select(Board).where(Board.id == board_id)
    board = db.exec(statement).first()
    return board

