from sqlmodel import SQLModel, select, Session

from backend.database.db_config import engine, admin_email, admin_password
from backend.models.role import Role, RolesEnum
from backend.models.user import User


def create_tables():
    SQLModel.metadata.create_all(engine)

def initialize_roles_and_permissions():
    with Session(engine) as db:

        for role in RolesEnum:
            role_obj = Role(name=role.value)
            db.add(role_obj)
            db.commit()

        admin_role_statement = select(Role).where(Role.name == "admin")
        role_admin = db.exec(admin_role_statement).first()
        admin_user = User(email=admin_email, name="Admin", hashed_password=admin_password, roles=[role_admin])
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

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