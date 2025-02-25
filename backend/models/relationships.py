from sqlmodel import SQLModel, Field

class UserRoleLink(SQLModel, table=True):
    user_id: int = Field(default=None, foreign_key="user.id", primary_key=True)
    role_id: int = Field(default=None, foreign_key="role.id", primary_key=True)

class UserBoardLink(SQLModel, table=True):
    user_id: int = Field(default=None, foreign_key="user.id", primary_key=True)
    board_id: int = Field(default=None, foreign_key="board.id", primary_key=True)
    role_id: int = Field(default=None, foreign_key="role.id")

class TaskCategoryLink(SQLModel, table=True):
    task_id: int = Field(default=None, foreign_key="task.id", primary_key=True)
    category_id: int = Field(default=None, foreign_key="taskcategory.id", primary_key=True)

class TaskBoardLink(SQLModel, table=True):
    task_id: int = Field(default=None, foreign_key="task.id", primary_key=True)
    board_id: int = Field(default=None, foreign_key="board.id", primary_key=True)

class TaskUserLink(SQLModel, table=True):
    task_id: int = Field(default=None, foreign_key="task.id", primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.id", primary_key=True)
