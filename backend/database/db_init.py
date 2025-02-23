from sqlmodel import  SQLModel,  select
from backend.models.role import Role
from backend.models.relationships import RolePermissionLink
from backend.models.permission import Permission
from sqlalchemy.exc import IntegrityError
from backend.database.db_config import engine
from sqlmodel import Session
from backend.database.role_enums import (
    RoleEnum, PERMISSION_ENUM, ROLE_PERMISSIONS_MAP
)

def create_tables():
    SQLModel.metadata.create_all(engine)


def initialize_roles_and_permissions():
    with Session(engine) as db:
        # Create roles in the database
        for role in RoleEnum:
            try:
                role_obj = Role(name=role.value)
                db.add(role_obj)
                db.commit()
            except IntegrityError:
                db.rollback()

        # Create permissions in the database
        for permission in PERMISSION_ENUM:
            try:
                permission_obj = Permission(name=permission.value)
                db.add(permission_obj)
                db.commit()
            except IntegrityError:
                db.rollback()

        for role_enum, permission_list in ROLE_PERMISSIONS_MAP.items():
            role_statement = select(Role).where(Role.name == role_enum.value)
            role_obj = db.exec(role_statement).first()
            if role_obj:
                for permission_enum in permission_list:
                    permission_statement = select(Permission).where(Permission.name == permission_enum.value)
                    permission_obj = db.exec(permission_statement).first()
                    if permission_obj:
                        role_permission_link = RolePermissionLink(
                            role_id=role_obj.id,
                            permission_id=permission_obj.id
                        )
                        db.add(role_permission_link)
                db.commit()

        db.close()
        print("Database initialized successfully.")


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