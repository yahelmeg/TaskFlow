from sqlmodel import SQLModel, Field

class UserRoleLink(SQLModel, table=True):
    user_id: int = Field(default=None, foreign_key="user.id", primary_key=True)
    role_id: int = Field(default=None, foreign_key="role.id", primary_key=True)

class UserTeamLink(SQLModel, table=True):
    user_id: int = Field(default=None, foreign_key="user.id", primary_key=True)
    team_id: int = Field(default=None, foreign_key="team.id", primary_key=True)

class TaskCategoryLink(SQLModel, table=True):
    task_id: int = Field(default=None, foreign_key="task.id", primary_key=True)
    category_id: int = Field(default=None, foreign_key="taskcategory.id", primary_key=True)

class RolePermissionLink(SQLModel, table=True):
    role_id: int = Field(default=None, foreign_key="role.id", primary_key=True)
    permission_id: int = Field(default=None, foreign_key="permission.id", primary_key=True)