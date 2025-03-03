import uvicorn
from fastapi import FastAPI

from backend.config import BACK_DOMAIN, BACK_PORT
from backend.routes.authentication import auth_router
from backend.routes.board import board_router
from backend.routes.invitation import invitation_router
from backend.routes.me import me_router
from backend.routes.user import user_router
from backend.routes.list import list_router
from backend.database.db_init import  delete_database, create_tables, initialize_roles_and_permissions

app = FastAPI()

delete_database()
create_tables()
initialize_roles_and_permissions()

routers = [ list_router, invitation_router, me_router, board_router, auth_router, user_router]

for router in routers:
    app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host=BACK_DOMAIN, port=BACK_PORT)


