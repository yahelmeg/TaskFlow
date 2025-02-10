from sqlmodel import create_engine, SQLModel, Session
import os
from dotenv import load_dotenv
from backend.models.role import Role, Permission
from sqlalchemy.exc import IntegrityError

load_dotenv()

postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")
postgres_host = os.getenv("POSTGRES_HOST")
postgres_port = os.getenv("POSTGRES_PORT")
postgres_db = os.getenv("POSTGRES_DB")
postgres_url = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
engine = create_engine(postgres_url)

def create_tables():
    SQLModel.metadata.create_all(engine)

def initialize_roles_and_permissions():

    session = Session(engine)
    roles = ["Admin", "Manager", "User"]

    permissions = [
        "create_user", "delete_user", "update_user",
        "create_task", "update_task", "assign_task", "delete_task",
        "create_comment", "delete_comments", "view_comments", "view_activities",
        "create_team", "add_user_to_team", "remove_user_from_team",
        "create_role", "create_permission", "delete_permissions", "assign_role",
    ]

    for role in roles:
        try:
            role_obj = Role(name=role)
            session.add(role_obj)
            session.commit()
        except IntegrityError:
            session.rollback()

    for permission in permissions:
        try:
            permission_obj = Permission(name=permission)
            session.add(permission_obj)
            session.commit()
        except IntegrityError:
            session.rollback()

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