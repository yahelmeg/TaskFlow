from sqlmodel import create_engine, SQLModel, Session, select
import os
from dotenv import load_dotenv
from backend.models.role import Role
from backend.models.relationships import RolePermissionLink
from backend.models.permission import Permission
from sqlalchemy.exc import IntegrityError
from contextlib import contextmanager
from fastapi import Depends
from db_dependencies import get_db


load_dotenv()

postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")
postgres_host = os.getenv("POSTGRES_HOST")
postgres_port = os.getenv("POSTGRES_PORT")
postgres_db = os.getenv("POSTGRES_DB")
postgres_url = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
engine = create_engine(postgres_url)

@contextmanager
def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


def create_tables():
    SQLModel.metadata.create_all(engine)

def initialize_roles_and_permissions(db=Depends(get_db)):

    with db as session:

        # Define roles and permissions
        roles = ["Admin", "User_Management", "Task_Management", "Comment_Management", "Team_Management", "Role_Management"]

        permissions = [
            "create_user", "delete_user", "update_user", "view_all_users",
            "create_task", "update_task", "assign_task", "delete_task", "view_all_tasks",
            "create_comment", "delete_comments", "view_activities",
            "create_team", "add_user_to_team", "remove_user_from_team",
            "create_role", "update_permission", "assign_role"
        ]

        # Create roles in the database
        for role in roles:
            try:
                role_obj = Role(name=role)
                session.add(role_obj)
                session.commit()
            except IntegrityError:
                session.rollback()

        # Create permissions in the database
        for permission in permissions:
            try:
                permission_obj = Permission(name=permission)
                session.add(permission_obj)
                session.commit()
            except IntegrityError:
                session.rollback()

        role_permission_map = {
            "Admin": permissions,
            "User_Management": [
                "create_user", "delete_user", "update_user", "view_all_users"
            ],
            "Task_Management": [
                "create_task", "update_task", "assign_task", "delete_task"
            ],
            "Comment_Management": [
                "create_comment", "delete_comments"
            ],
            "Team_Management": [
                "create_team", "add_user_to_team", "remove_user_from_team"
            ],
            "Role_Management": [
                "create_role", "update_permission", "assign_role"
            ]
        }

        for role_name, permission_for_role in role_permission_map.items():
            role_statement = select(Role).where(Role.name == role_name)
            role_obj = session.exec(role_statement).first()
            if role_obj:
                for permission_name in permission_for_role:
                    permission_statement=  select(Permission).where( Permission.name == permission_name)
                    permission_obj = session.exec(permission_statement).first()

                    if permission_obj:
                        role_permission_link = RolePermissionLink(role_id = role_obj.id ,permission_id = permission_obj.id)
                        session.add(role_permission_link)
                session.commit()

        session.close()


# Testing method, only used to test db initialization and reset the db.
def delete_database():
    try:
        confirmation = input("WARNING: This will delete all tables in the database. Are you sure? (yes/no): ").strip().lower()
        if confirmation == "yes":
            SQLModel.metadata.drop_all(engine)
            print("All tables have been deleted successfully.")
        else:
            print("Operation canceled. No tables were deleted.")
    except Exception as e:
        print(f"Error while deleting tables: {e}")