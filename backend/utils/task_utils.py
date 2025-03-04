from sqlmodel import Session, select

from backend.models.task import Task


def get_task_by_id(task_id: int, db: Session):
    list_statement = select(Task).where(Task.id == task_id)
    task = db.exec(list_statement).first()
    return task

def get_tasks_of_list(list_id: int, db: Session):
    tasks_statement = select(Task).where(Task.list_id == list_id)
    tasks = db.exec(tasks_statement).all()
    return tasks

def get_tasks_of_board(board_id: int, db: Session):
    tasks_statement = select(Task).where(Task.board_id == board_id)
    tasks = db.exec(tasks_statement).all()
    return tasks