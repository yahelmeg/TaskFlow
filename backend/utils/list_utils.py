from sqlmodel import Session, select, SQLModel

from backend.models.list import List


def get_list_by_id(list_id: int, db: Session):
    list_statement = select(List).where(List.id == list_id)
    db_list = db.exec(list_statement).first()
    return db_list

def get_lists_of_board(board_id: int, db: Session):
    lists_statement = select(List).where(List.board_id == board_id)
    lists = db.exec(lists_statement).all()
    return lists