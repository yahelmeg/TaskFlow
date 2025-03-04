from sqlmodel import Session, select, SQLModel

from backend.models.task_list import TaskList


def get_task_list_by_id( task_list_id: int, db : Session ) -> TaskList:
    statement = select(TaskList).where(TaskList.id == task_list_id)
    task_list = db.exec(statement).first()
    return task_list

def get_lists_of_board(board_id: int, db: Session):
    lists_statement = select(TaskList).where(TaskList.board_id == board_id)
    lists = db.exec(lists_statement).all()
    return lists


