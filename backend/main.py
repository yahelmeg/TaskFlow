import uvicorn
from fastapi import FastAPI

from backend.config import BACK_DOMAIN, BACK_PORT
from backend.routes.authentication import auth_router
from backend.routes.board import board_router
from backend.routes.me import me_router
from backend.routes.user import user_router

app = FastAPI()

#delete_database()
#create_tables()
#initialize_roles_and_permissions()

routers = [ me_router, board_router, auth_router, user_router]

for router in routers:
    app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to TaskFlow API!"}

if __name__ == "__main__":
    uvicorn.run(app, host=BACK_DOMAIN, port=BACK_PORT)


