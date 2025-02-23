from fastapi import FastAPI
from backend.database import create_tables, initialize_roles_and_permissions
import uvicorn
from backend.routes.user import user_router
from backend.routes.authentication import auth_router

app = FastAPI()

# delete_database()
create_tables()
initialize_roles_and_permissions()

routers = [ auth_router, user_router]

for router in routers:
    app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to TaskFlow API!"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)