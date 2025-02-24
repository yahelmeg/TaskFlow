from enum import Enum

class RoleEnum(str, Enum):
    ADMIN = "Admin"
    USER_READ = "User_Read"
    USER_WRITE = "User_Write"
    TASK_READ = "Task_Read"
    TASK_WRITE = "Task_Write"
    ACTIVITIES_READ = "Activities_Read"
    COMMENT_READ = "Comment_Read"
    COMMENT_WRITE = "Comment_Write"
    TEAM_READ = "Team_Read"
    TEAM_WRITE = "Team_Write"
    ROLE_READ = "Role_Read"
    ROLE_WRITE = "Role_Write"

class UserReadEnum(str, Enum):
    VIEW_USERS = "view_all_users"

class UserWriteEnum(str, Enum):
    CREATE_USER = "create_user"
    DELETE_USER = "delete_user"
    UPDATE_USER = "update_user"

class TaskReadEnum(str, Enum):
    VIEW_TASKS = "view_all_tasks"

class TaskWriteEnum(str, Enum):
    CREATE_TASK = "create_task"
    UPDATE_TASK = "update_task"
    ASSIGN_TASK = "assign_task"
    DELETE_TASK = "delete_task"

class CommentReadEnum(str, Enum):
    VIEW_COMMENTS = "view_comments"

class ActivityReadEnum(str, Enum):
    VIEW_ACTIVITY = "view_activities"

class CommentWriteEnum(str, Enum):
    CREATE_COMMENT = "create_comment"
    DELETE_COMMENT = "delete_comments"

class TeamReadEnum(str, Enum):
    VIEW_TEAMS = "view_teams"

class TeamWriteEnum(str, Enum):
    CREATE_TEAM = "create_team"
    ADD_USER_TO_TEAM = "add_user_to_team"
    REMOVE_USER_FROM_TEAM = "remove_user_from_team"

class RoleReadEnum(str, Enum):
    VIEW_ROLES = "view_roles"

class RoleWriteEnum(str, Enum):
    CREATE_ROLE = "create_role"
    UPDATE_PERMISSION = "update_permission"
    ASSIGN_ROLE = "assign_role"

PERMISSION_LIST = (
                list(UserReadEnum) + list(UserWriteEnum) + list(TaskReadEnum) + list(TaskWriteEnum) +
                list(CommentReadEnum) + list(CommentWriteEnum) + list(ActivityReadEnum) +
                list(TeamReadEnum) + list(TeamWriteEnum) + list(RoleReadEnum) + list(RoleWriteEnum)
        )

ROLE_PERMISSIONS_MAP = {
    RoleEnum.ADMIN: (
        list(UserReadEnum) + list(UserWriteEnum) +
        list(TaskReadEnum) + list(TaskWriteEnum) +
        list(ActivityReadEnum) + list(CommentReadEnum) + list(CommentWriteEnum) +
        list(TeamReadEnum) + list(TeamWriteEnum) +
        list(RoleReadEnum) + list(RoleWriteEnum)
    ),
    RoleEnum.USER_READ: list(UserReadEnum),
    RoleEnum.USER_WRITE: list(UserWriteEnum),
    RoleEnum.TASK_READ: list(TaskReadEnum),
    RoleEnum.TASK_WRITE: list(TaskWriteEnum),
    RoleEnum.ACTIVITIES_READ: list(ActivityReadEnum),
    RoleEnum.COMMENT_READ: list(CommentReadEnum),
    RoleEnum.COMMENT_WRITE: list(CommentWriteEnum),
    RoleEnum.TEAM_READ: list(TeamReadEnum),
    RoleEnum.TEAM_WRITE: list(TeamWriteEnum),
    RoleEnum.ROLE_READ: list(RoleReadEnum),
    RoleEnum.ROLE_WRITE: list(RoleWriteEnum),
}

